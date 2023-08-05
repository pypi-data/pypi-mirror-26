from pathlib import Path
import yaml
from os import path
import uuid
from urwid import MainLoop, ExitMainLoop
from functools import reduce

from .models import Note, Tag


class KeyHandler(object):

    def __init__(self, controller, config):
        self.controller = controller
        self.config = config
        self.editor = False

    def handle(self, input, *args, **kwargs):
        if self.is_keyboard_input(input):
            key = ''.join(input)
            self.handle_key(key)

    def is_key_bound(self, key, name):
        try:
            bound_keys = self.config.get_key_bindings()[name]
        except KeyError:
            return False
        else:
            return key in bound_keys

    def is_keyboard_input(self, input):
        if input:
            return reduce(lambda x, y: x and y,
                          map(lambda s: isinstance(s, str), input))

    def handle_key(self, key):
        if self.controller.editor_mode:
            size = 20
            self.editor.keypress(size, key)
            return

        if not self.controller.editor_mode:
            if self.is_key_bound(key, 'new_note'):
                self.controller.show_note_editor(
                    self.controller.edit_note_handler)
            elif self.is_key_bound(key, 'delete_note'):
                self.controller.delete_focused_note()
            elif self.is_key_bound(key, 'edit_note'):
                self.controller.show_note_editor(
                    self.controller.edit_note_handler, True)
            elif self.is_key_bound(key, 'increment_note_priority'):
                self.controller.increment_focused_note_priority()
            elif self.is_key_bound(key, 'decrement_note_priority'):
                self.controller.decrement_focused_note_priority()
            elif self.is_key_bound(key, 'quit'):
                self.controller.exit()
            elif self.is_key_bound(key, 'next_note'):
                self.controller.focus_next_note()
            elif self.is_key_bound(key, 'previous_note'):
                self.controller.focus_previous_note()


class Controller(object):

    def __init__(self, config, interface):
        self.config = config
        self.data_path = path.expanduser(self.config.get_data_path())
        self.notes = self.load_notes()
        self.tags = self.load_tags(self.notes)
        self.interface = interface
        self.editor_mode = False

        self.key_handler = KeyHandler(self, config)
        self.loop = MainLoop(interface,
                             config.get_palette(),
                             input_filter=self.key_handler.handle)
        self.refresh_interface()
        self.interface.focus_first_note()
        self.loop.run()

    def load_notes(self):
        # If no notes, create empty file
        if Path(self.data_path).is_file():
            with open(self.data_path, 'r') as data_file:
                note_yaml = yaml.load(data_file)
                notes = []

                if note_yaml is None:
                    return notes

                for unique_id, note in note_yaml.items():
                    notes.append(Note(note['title'],
                                      note['tags'],
                                      note['text'],
                                      note['priority'],
                                      unique_id))
                return notes
        else:
            open(self.data_path, 'x')
            return []

    def write_notes(self):
        with open(self.data_path, 'w') as data_file:
            for note in self.notes:
                yaml.dump(note.to_dictionary(),
                          data_file,
                          default_flow_style=False)

    def create_note(self, title, tags, text):
        note = Note(title, tags, text)
        self.notes.append(note)

    def delete_note(self, unique_id):
        for index, note in enumerate(self.notes):
            if note.id == unique_id:
                del self.notes[index]
                break

    def update_note(self, new_note):
        for index, note in enumerate(self.notes):
            if note.id == new_note.id:
                note = new_note
                break

    def delete_focused_note(self):
        note = self.interface.get_focused_note()
        self.delete_note(note.id)
        self.write_notes()

        self.refresh_interface()

    def load_tags(self, notes):
        tags = {'ALL': 0}
        tag_widgets = []
        for note in notes:
            tags['ALL'] += 1
            for tag in note.tags:
                if tag in tags:
                    tags[tag] += 1
                else:
                    tags[tag] = 1
        for tag in tags:
            tag_widgets.append(Tag(tag, tags[tag]))
        return tag_widgets

    def increment_focused_note_priority(self):
        note = self.interface.get_focused_note()
        note.increment_priority()
        self.write_notes()
        self.refresh_interface()

    def decrement_focused_note_priority(self):
        note = self.interface.get_focused_note()
        note.decrement_priority()
        self.write_notes()
        self.refresh_interface()

    def refresh_interface(self):
        self.interface.draw_notes(self.notes)
        self.tags = self.load_tags(self.notes)
        self.interface.draw_tags(self.tags)

    def show_note_editor(self, note_handler, edit_focused_note=False):
        note_to_edit = None
        if edit_focused_note:
            note_to_edit = self.interface.get_focused_note()
        self.editor_mode = True
        self.interface.show_note_editor(note_handler, note_to_edit)
        self.key_handler.editor = self.interface.get_note_editor()

    def edit_note_handler(self, note, original_note=None):
        if note is not None:
            title = note[0]
            tags = self._convert_tag_input(note[1])
            text = note[2]
            if original_note is not None:
                original_note.edit_note(title, tags, text)
                self.update_note(original_note)
            else:
                self.create_note(title, tags, text)
            self.write_notes()

            # Restart the loop.. Seems to work?
            self.loop.stop()
            self.loop.start()

        self.refresh_interface()
        self.editor_mode = False

    def _convert_tag_input(self, tag_text):
        split_tags = tag_text.split('//')
        return list(map(lambda tag: tag.strip(), split_tags))

    def exit(self):
        raise ExitMainLoop()

    def focus_next_note(self):
        self.interface.focus_next_note()

    def focus_previous_note(self):
        self.interface.focus_previous_note()
