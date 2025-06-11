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


app = tb.Window(themename="vapor")
app.title("Notatnik")
app.geometry("900x600")
app.minsize(700, 500)
app.style.configure('.', font=('Arial ', 13))

app.rowconfigure(0, weight=0)
app.columnconfigure(0, weight=3)
app.columnconfigure(1, weight=1)
app.rowconfigure(1, weight=0)
app.rowconfigure(2, weight=1)

top_frame = tk.Frame(app)
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

app.rowconfigure(2, weight=1)
app.columnconfigure(0, weight=3)
app.columnconfigure(1, weight=1)

search_frame = tk.Frame(app)
search_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 5))
search_frame.columnconfigure(1, weight=1)

tk.Label(search_frame, text="Szukaj:", font=("Arial", 12)).grid(row=0, column=0, padx=(0, 10))

search_var = tk.StringVar()
search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Arial", 12))
search_entry.grid(row=0, column=1, sticky="ew")

tk.Label(search_frame, text="Filtruj kategorię:", font=("Arial", 12)).grid(row=0, column=2, padx=(20, 10))
category_var = tk.StringVar()
category_options = [""] + ["Praca", "Osobiste", "Nauka"]
category_combo = ttk.Combobox(search_frame, textvariable=category_var, values=category_options, state="readonly",
                              font=("Arial", 12), width=15)
category_combo.grid(row=0, column=3, padx=(0, 10))

tk.Label(search_frame, text="Filtruj tagi (oddziel przecinkami):", font=("Arial", 12)).grid(row=0, column=4,
                                                                                            padx=(20, 10))
tags_var = tk.StringVar()
tags_entry = tk.Entry(search_frame, textvariable=tags_var, font=("Arial", 12), width=20)
tags_entry.grid(row=0, column=5, sticky="ew")

notes_frame = tk.Frame(app)
notes_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
notes_frame.rowconfigure(0, weight=1)
notes_frame.columnconfigure(0, weight=1)

empty_label = tk.Label(notes_frame, text="BRAK NOTATEK", font=("Segoe UI", 30, "bold"), )
empty_label.grid(row=0, column=0, sticky="nsew")

notes_container = tk.Frame(notes_frame)
notes_container.grid(row=0, column=0, sticky="nsew")

max_columns = 4
note_count = 0


def display_note(note_data):
    global note_count
    row = note_count // max_columns
    column = max_columns - 1 - (note_count % max_columns)
    bg_color = note_data.get("Kolor", "#FFFFFF")

    note_frame = tk.Frame(
        notes_container,
        width=250,
        height=250,
        relief="raised",
        borderwidth=2,
        bg=bg_color,
        cursor="hand2"
    )
    note_frame.grid(row=row, column=column, padx=10, pady=10)
    note_frame.pack_propagate(False)
    note_frame.configure(bg=bg_color)

    def on_enter(e):
        note_frame.config(relief="solid", borderwidth=3)

    def on_leave(e):
        note_frame.config(relief="raised", borderwidth=2)

    note_frame.bind("<Enter>", on_enter)
    note_frame.bind("<Leave>", on_leave)

    def open_note_info(note_data):
        info_win = tk.Toplevel(app)
        info_win.title(note_data.get("Tytuł", "Brak tytułu"))
        info_win.geometry("400x300")
        info_win.grab_set()

        tk.Label(info_win, text=note_data.get("Tytuł", ""), font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(info_win, text=f"Kategoria: {note_data.get('Kategoria', '')}", font=("Arial", 12, "italic")).pack(
            pady=5)

        tk.Label(info_win, text="Tagi:", font=("Arial", 12, "underline")).pack(anchor="w", padx=10)
        tags_frame = tk.Frame(info_win)
        tags_frame.pack(anchor="w", padx=10)
        for tag in note_data.get("Tagi", []):
            tk.Label(tags_frame, text=tag, borderwidth=1, relief="solid", padx=5, pady=2).pack(side="left", padx=2,
                                                                                               pady=2)

        if "Zawartość" in note_data:
            content_text = tk.Text(info_win, wrap="word", height=10)
            content_text.pack(fill="both", expand=True, padx=10, pady=10)
            content_text.insert("1.0", note_data["Zawartość"])
            content_text.config(state="disabled")

    def on_click(e):
        if is_deleting:
            confirm_delete(note_data)
        elif is_editing:
            open_note_editor(note_data)
        else:
            open_note_info(note_data)

    note_frame.bind("<Button-1>", on_click)

    title_label = tk.Label(
        note_frame,
        text=note_data["Tytuł"],
        font=("Arial", 14, "bold"),
        wraplength=230,
        bg=bg_color
    )
    title_label.pack(pady=(10, 5))

    tags_frame = tk.Frame(note_frame, bg=bg_color)
    tags_frame.pack(pady=5)

    colors = ["#FF6666", "#66CC66", "#6699FF", "#FFCC33", "#3399FF", "#FF33AA"]
    for i, tag in enumerate(note_data["Tagi"]):
        color = colors[i % len(colors)]
        tag_label = tk.Label(
            tags_frame,
            text=tag,
            bg=color,
            padx=6,
            pady=2,
            borderwidth=1,
            relief="solid"
        )
        tag_label.pack(side="left", padx=3)
    note_frame.custom_bg_color = bg_color

    category_label = tk.Label(
        note_frame,
        text=f"Kategoria: {note_data['Kategoria']}",
        font=("Arial", 10, "italic"),
        bg=bg_color
    )
    category_label.pack(side="bottom", pady=(10, 5))

    note_count += 1


def load_saved_notes(filter_text="", category_filter="", tags_filter=None):
    global note_count
    for widget in notes_container.winfo_children():
        widget.destroy()
    note_count = 0

    saved_notes = load_notes()
    filtered_notes = []
    filter_text_lower = filter_text.lower()
    category_filter_lower = category_filter.lower()
    tags_filter_lower = [tag.strip().lower() for tag in tags_filter] if tags_filter else []

    for note_data in saved_notes:
        title = note_data.get("Tytuł", "").lower()
        tags = [tag.lower() for tag in note_data.get("Tagi", [])]
        category = note_data.get("Kategoria", "").lower()
        content = note_data.get("Zawartość", "").lower()

        if (filter_text_lower in title or
                any(filter_text_lower in tag for tag in tags) or
                filter_text_lower in category or
                filter_text_lower in content):

            if category_filter_lower and category != category_filter_lower:
                continue

            if tags_filter_lower:
                if not all(tag in tags for tag in tags_filter_lower):
                    continue

            filtered_notes.append(note_data)

    if filtered_notes:
        if empty_label.winfo_ismapped():
            empty_label.grid_forget()
        for note_data in filtered_notes:
            display_note(note_data)
    else:
        empty_label.grid(row=0, column=0, sticky="nsew")


def on_filters_change(*args):
    filter_text = search_var.get()
    category_filter = category_var.get()
    tags_filter = [tag.strip() for tag in tags_var.get().split(",") if tag.strip()]
    load_saved_notes(filter_text, category_filter, tags_filter)


search_var.trace_add("write", on_filters_change)
category_var.trace_add("write", on_filters_change)
tags_var.trace_add("write", on_filters_change)


def open_note_creator():
    def on_save(note_data):
        if empty_label.winfo_ismapped():
            empty_label.grid_forget()
        save_note_to_file(note_data)
        display_note(note_data)

    note_creator = NoteCreator(app, categories=["Praca", "Osobiste", "Nauka"], on_save=on_save)
    note_creator.grab_set()


def remove_note(note_data):
    global is_deleting
    notes = load_notes()
    notes = [note for note in notes if note.get("id") != note_data.get("id")]

    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=4)

    for widget in notes_container.winfo_children():
        widget.destroy()

    global note_count
    note_count = 0
    load_saved_notes()

    is_deleting = False
    btn_left_2.config(bootstyle="danger-outline")


is_deleting = False


def toggle_delete_mode():
    global is_deleting, is_editing

    if is_editing:  
        is_editing = False
        btn_left_3.config(bootstyle="primary-outline")

    is_deleting = not is_deleting
    btn_left_2.config(bootstyle="danger" if is_deleting else "danger-outline")


def confirm_delete(note_data):
    confirm_win = tk.Toplevel(app)
    confirm_win.title("Potwierdzenie usunięcia")
    confirm_win.geometry("300x150")
    confirm_win.grab_set()

    tk.Label(confirm_win, text=f"Czy na pewno chcesz usunąć notatkę: {note_data['Tytuł']}?", font=("Arial", 12)).pack(
        pady=10)

    btn_yes = tk.Button(confirm_win, text="Tak", command=lambda: [remove_note(note_data), confirm_win.destroy()])
    btn_no = tk.Button(confirm_win, text="Nie", command=confirm_win.destroy)

    btn_yes.pack(side="left", padx=20, pady=10)
    btn_no.pack(side="right", padx=20, pady=10)


is_editing = False


def toggle_edit_mode():
    global is_editing, is_deleting

    if is_deleting:  
        is_deleting = False
        btn_left_2.config(bootstyle="danger-outline")

    is_editing = not is_editing
    btn_left_3.config(bootstyle="primary" if is_editing else "primary-outline")


def open_note_editor(note_data):
    def on_save_edited_note(updated_note_data):
        notes = load_notes()
        for i, note in enumerate(notes):
            if note.get("id") == updated_note_data.get("id"):
                notes[i] = updated_note_data
                break

        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=4)

        for widget in notes_container.winfo_children():
            widget.destroy()

        global note_count
        note_count = 0
        load_saved_notes()
        toggle_edit_mode()

    NoteCreator(app, categories=["Praca", "Osobiste", "Nauka"], on_save=on_save_edited_note,
                note_data=note_data).grab_set()


btn_left_1.config(command=open_note_creator)
btn_left_2.config(command=toggle_delete_mode)
btn_left_3.config(command=toggle_edit_mode)

def refresh_notes_colors():
    for note_frame in notes_container.winfo_children():
        bg_color = getattr(note_frame, "custom_bg_color", "#FFFFFF")
        note_frame.configure(bg=bg_color)
        for child in note_frame.winfo_children():
            try:
                child.configure(bg=bg_color)
            except:
                pass
def toggle_theme():
    current_theme = app.style.theme_use()
    new_theme = "vapor" if current_theme != "vapor" else "morph"
    app.style.theme_use(new_theme)
    refresh_notes_colors()

def integrate_calendar():
    tk.messagebox.showinfo("Integracja z kalendarzem", "Funkcja w budowie")


def export_pdf():
    tk.messagebox.showinfo("Eksport do PDF", "Funkcja w budowie")

btn_right_1.config(command=toggle_theme)
btn_right_2.config(command=integrate_calendar)
btn_right_3.config(command=export_pdf)

if __name__ == "__main__":
    load_saved_notes()
    app.mainloop()
