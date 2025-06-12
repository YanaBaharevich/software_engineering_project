import json
import os

NOTES_FILE = "saved_notes.json"
is_deleting = False
is_editing = False
last_id = 0

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


