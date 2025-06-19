import json
import os

NOTES_FILE = "saved_notes.json"
_is_deleting = False
_is_editing = False

def is_deleting():
    return _is_deleting

def set_deleting(value):
    global _is_deleting
    _is_deleting = value

def is_editing():
    return _is_editing

def set_editing(value):
    global _is_editing
    _is_editing = value

def load_notes():
    global last_id
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            notes = json.load(f)
            if notes:
                last_id = max(note.get("id", 0) for note in notes)
            return notes
    return []

def save_note_to_file(note_data):
    notes = load_notes()
    notes.append(note_data)
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=4)

