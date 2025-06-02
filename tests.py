import unittest
import json
import os
import tempfile
from unittest.mock import patch
import datetime


class TestNotesApp(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_notes_file = os.path.join(self.temp_dir, "test_notes.json")

        self.sample_notes = [
            {
                "id": 1,
                "Tytuł": "Notatka testowa 1",
                "Zawartość": "Treść 1",
                "Kategoria": "Praca",
                "Tagi": ["wazne", "praca"],
                "KodPIN": "1234",
                "Przypomnienie": "2024-12-25",
                "Kolor": "#FFFFFF",
                "created": "2024-01-01",
                "modified": "2024-01-01"
            },
            {
                "id": 2,
                "Tytuł": "Notatka testowa 2",
                "Zawartość": "Treść 2",
                "Kategoria": "Osobiste",
                "Tagi": ["osobiste"],
                "KodPIN": "",
                "Przypomnienie": "",
                "Kolor": "#FFFF00",
                "created": "2024-01-02",
                "modified": "2024-01-02"
            }
        ]

    def tearDown(self):
        if os.path.exists(self.test_notes_file):
            os.remove(self.test_notes_file)
        os.rmdir(self.temp_dir)

    def test_load_notes_file_exists(self):
        with open(self.test_notes_file, "w", encoding="utf-8") as f:
            json.dump(self.sample_notes, f, ensure_ascii=False, indent=4)

        with patch('body.NOTES_FILE', self.test_notes_file):
            from body import load_notes
            notes = load_notes()

        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[0]["Tytuł"], "Notatka testowa 1")
        self.assertEqual(notes[1]["Kategoria"], "Osobiste")

    def test_load_notes_file_not_exists(self):
        non_existent_file = os.path.join(self.temp_dir, "non_existent.json")

        with patch('body.NOTES_FILE', non_existent_file):
            from body import load_notes
            notes = load_notes()

        self.assertEqual(notes, [])

    def test_load_notes_empty_file(self):
        with open(self.test_notes_file, "w", encoding="utf-8") as f:
            json.dump([], f)

        with patch('body.NOTES_FILE', self.test_notes_file):
            from body import load_notes
            notes = load_notes()

        self.assertEqual(notes, [])

    def test_save_note_to_file_new_note(self):
        new_note = {
            "id": 3,
            "Tytuł": "Nowa notatka",
            "Zawartość": "treść",
            "Kategoria": "Nauka",
            "Tagi": ["nauka"],
            "KodPIN": "",
            "Przypomnienie": "",
            "Kolor": "#00FF00",
            "created": "2024-01-03",
            "modified": "2024-01-03"
        }

        with open(self.test_notes_file, "w", encoding="utf-8") as f:
            json.dump(self.sample_notes, f, ensure_ascii=False, indent=4)

        with patch('body.NOTES_FILE', self.test_notes_file):
            from body import save_note_to_file
            save_note_to_file(new_note)

        with open(self.test_notes_file, "r", encoding="utf-8") as f:
            notes = json.load(f)

        self.assertEqual(len(notes), 3)
        self.assertEqual(notes[2]["Tytuł"], "Nowa notatka")

    def test_save_note_to_file_empty_file(self):
        new_note = self.sample_notes[0]

        with patch('body.NOTES_FILE', self.test_notes_file):
            from body import save_note_to_file
            save_note_to_file(new_note)

        with open(self.test_notes_file, "r", encoding="utf-8") as f:
            notes = json.load(f)

        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["Tytuł"], "Notatka testowa 1")


class TestNoteFiltering(unittest.TestCase):

    def setUp(self):
        self.sample_notes = [
            {
                "id": 1,
                "Tytuł": "Praca nad projektem",
                "Zawartość": "Trzeba dokończyć prezentację",
                "Kategoria": "Praca",
                "Tagi": ["pilne", "projekt"]
            },
            {
                "id": 2,
                "Tytuł": "Zakupy",
                "Zawartość": "Kupić mleko i chleb",
                "Kategoria": "Osobiste",
                "Tagi": ["dom", "zakupy"]
            },
            {
                "id": 3,
                "Tytuł": "Nauka Pythona",
                "Zawartość": "Powtórzyć podstawy OOP",
                "Kategoria": "Nauka",
                "Tagi": ["programowanie", "python"]
            }
        ]

    def test_filter_by_text(self):

        def filter_notes(notes, filter_text):
            filter_text_lower = filter_text.lower()
            filtered = []
            for note in notes:
                title = note.get("Tytuł", "").lower()
                content = note.get("Zawartość", "").lower()
                tags = [tag.lower() for tag in note.get("Tagi", [])]
                category = note.get("Kategoria", "").lower()

                if (filter_text_lower in title or
                        filter_text_lower in content or
                        any(filter_text_lower in tag for tag in tags) or
                        filter_text_lower in category):
                    filtered.append(note)
            return filtered

        result = filter_notes(self.sample_notes, "praca")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 1)

        result = filter_notes(self.sample_notes, "mleko")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 2)

        result = filter_notes(self.sample_notes, "python")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 3)

    def test_filter_by_category(self):

        def filter_by_category(notes, category_filter):
            if not category_filter:
                return notes
            return [note for note in notes if note.get("Kategoria", "").lower() == category_filter.lower()]

        result = filter_by_category(self.sample_notes, "Praca")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Kategoria"], "Praca")

        result = filter_by_category(self.sample_notes, "")
        self.assertEqual(len(result), 3)

    def test_filter_by_tags(self):

        def filter_by_tags(notes, tags_filter):
            if not tags_filter:
                return notes
            tags_filter_lower = [tag.strip().lower() for tag in tags_filter]
            filtered = []
            for note in notes:
                note_tags = [tag.lower() for tag in note.get("Tagi", [])]
                if all(tag in note_tags for tag in tags_filter_lower):
                    filtered.append(note)
            return filtered

        result = filter_by_tags(self.sample_notes, ["projekt"])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 1)

        result = filter_by_tags(self.sample_notes, ["javascript"])
        self.assertEqual(len(result), 0)


class TestNoteCreatorLogic(unittest.TestCase):

    def test_note_data_creation(self):

        def create_note_data(title, content, category, tags, pin="", reminder="", color="#FFFFFF"):
            return {
                "Tytuł": title.strip(),
                "Zawartość": content.strip(),
                "Kategoria": category,
                "Tagi": tags,
                "KodPIN": pin.strip(),
                "Przypomnienie": reminder.strip(),
                "Kolor": color,
                "created": datetime.datetime.now().strftime("%Y-%m-%d"),
                "modified": datetime.datetime.now().strftime("%Y-%m-%d")
            }

        note = create_note_data(
            title="Test",
            content="Treść testu",
            category="Praca",
            tags=["test", "praca"]
        )

        self.assertEqual(note["Tytuł"], "Test")
        self.assertEqual(note["Zawartość"], "Treść testu")
        self.assertEqual(note["Kategoria"], "Praca")
        self.assertEqual(len(note["Tagi"]), 2)
        self.assertEqual(note["Kolor"], "#FFFFFF")

class TestNoteOperations(unittest.TestCase):

    def setUp(self):
        self.sample_notes = [
            {"id": 1, "Tytuł": "Notatka 1", "Kategoria": "Praca"},
            {"id": 2, "Tytuł": "Notatka 2", "Kategoria": "Osobiste"},
            {"id": 3, "Tytuł": "Notatka 3", "Kategoria": "Nauka"}
        ]

    def test_find_note_by_id(self):

        def find_note_by_id(notes, note_id):
            for note in notes:
                if note.get("id") == note_id:
                    return note
            return None

        note = find_note_by_id(self.sample_notes, 2)
        self.assertIsNotNone(note)
        self.assertEqual(note["Tytuł"], "Notatka 2")

        note = find_note_by_id(self.sample_notes, 999)
        self.assertIsNone(note)

    def test_remove_note_by_id(self):

        def remove_note_by_id(notes, note_id):
            return [note for note in notes if note.get("id") != note_id]

        updated_notes = remove_note_by_id(self.sample_notes, 2)
        self.assertEqual(len(updated_notes), 2)

        ids = [note["id"] for note in updated_notes]
        self.assertNotIn(2, ids)
        self.assertIn(1, ids)
        self.assertIn(3, ids)

    def test_update_note(self):

        def update_note(notes, updated_note):
            for i, note in enumerate(notes):
                if note.get("id") == updated_note.get("id"):
                    notes[i] = updated_note
                    return True
            return False

        updated_note = {
            "id": 2,
            "Tytuł": "Edytowana notatka 2",
            "Kategoria": "Nauka"
        }

        notes_copy = self.sample_notes.copy()
        result = update_note(notes_copy, updated_note)

        self.assertTrue(result)
        self.assertEqual(notes_copy[1]["Tytuł"], "Edytowana notatka 2")
        self.assertEqual(notes_copy[1]["Kategoria"], "Nauka")

    def test_get_next_id(self):

        def get_next_id(notes):
            if not notes:
                return 1
            return max(note.get("id", 0) for note in notes) + 1

        next_id = get_next_id(self.sample_notes)
        self.assertEqual(next_id, 4)

        next_id = get_next_id([])
        self.assertEqual(next_id, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
