import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from note_creator import NoteCreator
import json
import os

NOTES_FILE = "saved_notes.json"
def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
def save_note_to_file(note_data):
    notes = load_notes()
    notes.append(note_data)
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=4)



app = tb.Window(themename="vapor")
app.title("Notatnik")
app.geometry("900x600")
app.minsize(700, 500)
app.style.configure('.', font=('Arial ', 13))

app.rowconfigure(0, weight=0)     # Zona przycisków
app.columnconfigure(0, weight=3)  # Lewa
app.columnconfigure(1, weight=1)  # Prawa
app.rowconfigure(1, weight=0)
app.rowconfigure(2, weight=1)     # Zona notatek

top_frame = tb.Frame(app)
top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
top_frame.columnconfigure(0, weight=3)
top_frame.columnconfigure(1, weight=1)

left_buttons_frame = tb.Frame(top_frame)
left_buttons_frame.grid(row=0, column=0, sticky="w")

btn_left_1 = tb.Button(left_buttons_frame, text="Dodaj notatkę", bootstyle="success-outline")
btn_left_2 = tb.Button(left_buttons_frame, text="Usuń notatkę", bootstyle="danger-outline")
btn_left_3 = tb.Button(left_buttons_frame, text="Edytuj notatkę", bootstyle="primary-outline")
btn_left_1.pack(side="left", padx=5)
btn_left_2.pack(side="left", padx=5)
btn_left_3.pack(side="left", padx=5)

right_buttons_frame = tb.Frame(top_frame)
right_buttons_frame.grid(row=0, column=1, sticky="e")

btn_right_1 = tb.Button(right_buttons_frame, text="Zmień tryb na jasny/ciemny", bootstyle="info-outline")
btn_right_2 = tb.Button(right_buttons_frame, text="Zintegruj z kalendarzem", bootstyle="primary-outline")
btn_right_3 = tb.Button(right_buttons_frame, text="Eksportuj do PDF", bootstyle="primary-outline")

btn_right_1.pack(side="top", fill="x", pady=5)
btn_right_2.pack(side="top", fill="x", pady=5)
btn_right_3.pack(side="top", fill="x", pady=5)

separator = ttk.Separator(app, orient='horizontal')
separator.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10)

notes_frame = tb.Frame(app)
notes_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

app.rowconfigure(2, weight=1)
app.columnconfigure(0, weight=3)
app.columnconfigure(1, weight=1)
notes_frame.rowconfigure(0, weight=1)
notes_frame.columnconfigure(0, weight=1)

empty_label = tk.Label(notes_frame, text="BRAK NOTATEK",
                 font=("Segoe UI", 30, "bold"),)
empty_label.grid(row=0, column=0, sticky="nsew")

notes_container = tb.Frame(notes_frame)
notes_container.grid(row=0, column=0, sticky="nsew")

max_columns = 4
note_count = 0

# lodowanie notatek
def display_note(note_data):
    global note_count
    row = note_count // max_columns
    column = max_columns - 1 - (note_count % max_columns)

    note_frame = tb.Frame(
        notes_container,
        width=250,
        height=250,
        relief="raised",
        borderwidth=2
    )
    note_frame.grid(row=row, column=column, padx=10, pady=10)
    note_frame.pack_propagate(False)

    title_label = tb.Label(note_frame, text=note_data["title"], font=("Arial", 14, "bold"), wraplength=230)
    title_label.pack(pady=(10, 5))

    tags_frame = tb.Frame(note_frame)
    tags_frame.pack(pady=5)
    colors = ["#FF6666", "#66CC66", "#6699FF", "#FFCC33", "#3399FF", "#FF33AA"]
    for i, tag in enumerate(note_data["tags"]):
        color = colors[i % len(colors)]
        tag_label = tk.Label(
            tags_frame,
            text=tag,
            bg=color,
            fg="black",
            font=("Arial", 10, "bold"),
            padx=6,
            pady=2,
            borderwidth=1,
            relief="solid"
        )
        tag_label.pack(side="left", padx=3)

    category_label = tb.Label(note_frame, text=f"Kategoria: {note_data['category']}", font=("Arial", 10, "italic"))
    category_label.pack(side="bottom", pady=(10, 5))

    note_count += 1


def load_saved_notes():
    global note_count
    saved_notes = load_notes()
    if saved_notes:
        if empty_label.winfo_ismapped():
            empty_label.grid_forget()
    for note_data in saved_notes:
        display_note(note_data)


def open_note_creator():
    def on_save(note_data):
        if empty_label.winfo_ismapped():
            empty_label.grid_forget()
        save_note_to_file(note_data)
        display_note(note_data)
    note_creator = NoteCreator(app, categories=["Praca", "Osobiste", "Nauka"], on_save=on_save)
    note_creator.grab_set()


btn_left_1.config(command=open_note_creator)
load_saved_notes()
app.mainloop()

