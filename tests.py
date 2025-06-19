import unittest
import json
import os
import tempfile
from unittest.mock import patch, MagicMock
import datetime
from storage import load_notes, save_note_to_file, is_deleting, set_deleting, is_editing, set_editing
from actions import remove_note, reset_modes, integrate_database, export_pdf
from note_creator import NoteCreator

class TestStorageFunctions(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_notes_file = os.path.join(self.temp_dir, "test_notes.json")
        self.sample_notes = [
            {
                "id": 1,
                "Tytuł": "Test Note 1",
                "Zawartość": "Content 1",
                "Kategoria": "Praca",
                "Tagi": ["tag1"],
                "KodPIN": "1234",
                "Przypomnienie": "2024-01-01",
                "Kolor": "#FFFFFF",
                "created": "2024-01-01",
                "modified": "2024-01-01"
            }
        ]
        self.patcher = patch('storage.NOTES_FILE', self.test_notes_file)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        if os.path.exists(self.test_notes_file):
            os.remove(self.test_notes_file)
        os.rmdir(self.temp_dir)

    def test_load_notes_existing_file(self):
        with open(self.test_notes_file, 'w', encoding='utf-8') as f:
            json.dump(self.sample_notes, f)

        notes = load_notes()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]['Tytuł'], "Test Note 1")

    def test_load_notes_non_existing_file(self):
        notes = load_notes()
        self.assertEqual(notes, [])

    def test_save_note_to_file(self):
        save_note_to_file(self.sample_notes[0])

        with open(self.test_notes_file, 'r', encoding='utf-8') as f:
            notes = json.load(f)

        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]['Tytuł'], "Test Note 1")

    def test_delete_mode_functions(self):
        self.assertFalse(is_deleting())
        set_deleting(True)
        self.assertTrue(is_deleting())
        set_deleting(False)
        self.assertFalse(is_deleting())

    def test_edit_mode_functions(self):
        self.assertFalse(is_editing())
        set_editing(True)
        self.assertTrue(is_editing())
        set_editing(False)
        self.assertFalse(is_editing())


class TestActionsFunctions(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_notes_file = os.path.join(self.temp_dir, "test_notes.json")
        self.sample_notes = [
            {
                "id": 1,
                "Tytuł": "Test Note 1",
                "Zawartość": "Content 1",
                "Kategoria": "Praca",
                "Tagi": ["tag1"],
                "KodPIN": "1234",
                "Przypomnienie": "2024-01-01",
                "Kolor": "#FFFFFF",
                "created": "2024-01-01",
                "modified": "2024-01-01"
            },
            {
                "id": 2,
                "Tytuł": "Test Note 2",
                "Zawartość": "Content 2",
                "Kategoria": "Osobiste",
                "Tagi": ["tag2"],
                "KodPIN": "",
                "Przypomnienie": "",
                "Kolor": "#FFFF00",
                "created": "2024-01-02",
                "modified": "2024-01-02"
            }
        ]

        with open(self.test_notes_file, 'w', encoding='utf-8') as f:
            json.dump(self.sample_notes, f)

        self.patcher = patch('storage.NOTES_FILE', self.test_notes_file)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        if os.path.exists(self.test_notes_file):
            os.remove(self.test_notes_file)
        os.rmdir(self.temp_dir)

    def test_remove_note(self):
        note_to_remove = self.sample_notes[0]
        notes = load_notes()
        notes = [note for note in notes if note["id"] != note_to_remove["id"]]
        with open(self.test_notes_file, 'w', encoding='utf-8') as f:
            json.dump(notes, f, ensure_ascii=False, indent=4)
        notes = load_notes()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]['id'], 2)

    def test_reset_modes(self):
        set_deleting(True)
        set_editing(True)
        reset_modes()
        self.assertFalse(is_deleting())
        self.assertFalse(is_editing())

    @patch('pyodbc.connect')
    def test_integrate_database(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        integrate_database()

        self.assertTrue(mock_cursor.execute.called)
        self.assertTrue(mock_conn.commit.called)

class TestNoteCreator(unittest.TestCase):
    @patch('tkinter.Toplevel')
    def test_note_creator_init(self, mock_toplevel):
        parent = MagicMock()
        categories = ["Praca", "Osobiste"]
        on_save = MagicMock()
        note_data = None

        creator = NoteCreator(parent, categories, on_save, note_data)

        self.assertIsNotNone(creator)
        self.assertEqual(creator.categories, categories)
        self.assertEqual(creator.on_save, on_save)

    @patch('tkinter.Toplevel')
    def test_note_creator_with_data(self, mock_toplevel):
        parent = MagicMock()
        categories = ["Praca", "Osobiste"]
        on_save = MagicMock()
        note_data = {
            "id": 1,
            "Tytuł": "Test Note",
            "Zawartość": "Test Content",
            "Kategoria": "Praca",
            "Tagi": ["tag1"],
            "KodPIN": "1234",
            "Przypomnienie": "2024-01-01",
            "Kolor": "#FFFFFF",
            "created": "2024-01-01",
            "modified": "2024-01-01"
        }

        creator = NoteCreator(parent, categories, on_save, note_data)

        self.assertIsNotNone(creator)
        self.assertEqual(creator.note_data, note_data)


if __name__ == '__main__':
    unittest.main()

