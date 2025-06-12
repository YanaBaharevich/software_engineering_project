import tkinter as tk
import json
import os
from storage import load_notes, is_deleting, is_editing
from storage import save_note_to_file
from note_creator import NoteCreator

def toggle_delete_mode():
    global is_deleting, is_editing
    if is_editing:
        is_editing = False
    is_deleting = not is_deleting

def toggle_edit_mode():
    global is_editing, is_deleting
    if is_deleting:
        is_deleting = False
    is_editing = not is_editing

def confirm_delete(note_data):
    confirm_win = tk.Toplevel()
    confirm_win.title("Potwierdzenie usunięcia")
    confirm_win.geometry("300x150")
    confirm_win.grab_set()
    tk.Label(confirm_win, text=f"Czy na pewno chcesz usunąć notatkę: {note_data['Tytuł']}?", font=("Arial", 12)).pack(pady=10)
    tk.Button(confirm_win, text="Tak", command=lambda: [remove_note(note_data), confirm_win.destroy()]).pack(side="left", padx=20, pady=10)
    tk.Button(confirm_win, text="Nie", command=confirm_win.destroy).pack(side="right", padx=20, pady=10)

def remove_note(note_data):
    notes = load_notes()
    notes = [note for note in notes if note.get("id") != note_data.get("id")]
    with open("saved_notes.json", "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=4)

def open_note_editor(note_data):
    def on_save_edited_note(updated_note_data):
        notes = load_notes()
        for i, note in enumerate(notes):
            if note.get("id") == updated_note_data.get("id"):
                notes[i] = updated_note_data
                break
        with open("saved_notes.json", "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=4)

    NoteCreator(None, categories=["Praca", "Osobiste", "Nauka"], on_save=on_save_edited_note, note_data=note_data).grab_set()

def toggle_theme(app, refresh_notes_colors):
    current_theme = app.style.theme_use()
    new_theme = "vapor" if current_theme != "vapor" else "morph"
    app.style.theme_use(new_theme)
    refresh_notes_colors()

def integrate_calendar():
    tk.messagebox.showinfo("Integracja z kalendarzem", "Funkcja w budowie")

def export_pdf():
    tk.messagebox.showinfo("Eksport do PDF", "Funkcja w budowie")