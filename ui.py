import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Frame, Button
from ttkbootstrap.constants import *
from window import set_context, load_saved_notes
from actions import toggle_delete_mode, toggle_edit_mode, toggle_theme, integrate_database, export_pdf
from note_creator import NoteCreator
from storage import save_note_to_file, is_deleting, is_editing, set_editing, set_deleting


def build_interface(app):
    app.style.configure('.', font=('Arial ', 13))
    app.rowconfigure(0, weight=0)
    app.columnconfigure(0, weight=3)
    app.columnconfigure(1, weight=1)
    app.rowconfigure(1, weight=0)
    app.rowconfigure(2, weight=1)
    search_var = tk.StringVar()
    category_var = tk.StringVar()
    tags_var = tk.StringVar()

    top_frame = tk.Frame(app)
    top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
    top_frame.columnconfigure(0, weight=3)
    top_frame.columnconfigure(1, weight=1)

    left_buttons_frame = Frame(top_frame)
    left_buttons_frame.grid(row=0, column=0, sticky="w")

    btn_left_1 = Button(left_buttons_frame, text="Dodaj notatkę", bootstyle="success-outline")
    btn_left_2 = Button(left_buttons_frame, text="Usuń notatkę", bootstyle="danger-outline")
    btn_left_3 = Button(left_buttons_frame, text="Edytuj notatkę", bootstyle="primary-outline")
    btn_left_1.pack(side="left", padx=5)
    btn_left_2.pack(side="left", padx=5)
    btn_left_3.pack(side="left", padx=5)

    right_buttons_frame = Frame(top_frame)
    right_buttons_frame.grid(row=0, column=1, sticky="e")

    btn_right_1 = Button(right_buttons_frame, text="Zmień tryb na jasny/ciemny", bootstyle="info-outline")
    btn_right_2 = Button(right_buttons_frame, text="Zapisz w bazie", bootstyle="primary-outline")
    btn_right_3 = Button(right_buttons_frame, text="Eksportuj do PDF", bootstyle="primary-outline")
    btn_right_1.pack(side="top", fill="x", pady=5)
    btn_right_2.pack(side="top", fill="x", pady=5)
    btn_right_3.pack(side="top", fill="x", pady=5)

    separator = ttk.Separator(app, orient='horizontal')
    separator.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10)

    search_frame = tk.Frame(app)
    search_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 5))
    search_frame.columnconfigure(1, weight=1)

    tk.Label(search_frame, text="Szukaj:", font=("Arial", 12)).grid(row=0, column=0, padx=(0, 10))
    search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Arial", 12))
    search_entry.grid(row=0, column=1, sticky="ew")

    tk.Label(search_frame, text="Filtruj kategorię:", font=("Arial", 12)).grid(row=0, column=2, padx=(20, 10))
    category_options = [""] + ["Praca", "Osobiste", "Nauka"]
    category_combo = ttk.Combobox(search_frame, textvariable=category_var, values=category_options, state="readonly", font=("Arial", 12), width=15)
    category_combo.grid(row=0, column=3, padx=(0, 10))

    tk.Label(search_frame, text="Filtruj tagi (oddziel przecinkami):", font=("Arial", 12)).grid(row=0, column=4, padx=(20, 10))
    tags_entry = tk.Entry(search_frame, textvariable=tags_var, font=("Arial", 12), width=20)
    tags_entry.grid(row=0, column=5, sticky="ew")

    notes_frame = tk.Frame(app)
    notes_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
    notes_frame.rowconfigure(0, weight=1)
    notes_frame.columnconfigure(0, weight=1)

    empty_label = tk.Label(notes_frame, text="BRAK NOTATEK", font=("Segoe UI", 30, "bold"))
    empty_label.grid(row=0, column=0, sticky="nsew")

    notes_container = tk.Frame(notes_frame)
    notes_container.grid(row=0, column=0, sticky="nsew")

    set_context(notes_container, empty_label, app)

    def refresh_notes():
        filter_text = search_var.get()
        category_filter = category_var.get()
        tags_filter = [tag.strip() for tag in tags_var.get().split(",") if tag.strip()]
        load_saved_notes(filter_text, category_filter, tags_filter)


    def on_filters_change(*args):
        filter_text = search_var.get()
        category_filter = category_var.get()
        tags_filter = [tag.strip() for tag in tags_var.get().split(",") if tag.strip()]
        load_saved_notes(filter_text, category_filter, tags_filter)

    def open_note_creator():
        def on_save(note_data):
            if empty_label.winfo_ismapped():
                empty_label.grid_forget()
            save_note_to_file(note_data)
            refresh_notes()

        NoteCreator(app, categories=["Praca", "Osobiste", "Nauka"], on_save=on_save).grab_set()

    search_var.trace_add("write", on_filters_change)
    category_var.trace_add("write", on_filters_change)
    tags_var.trace_add("write", on_filters_change)

    btn_left_1.config(command=open_note_creator)
    btn_left_2.config(command=lambda: toggle_delete_mode(refresh_notes))

    btn_right_1.config(command=lambda: toggle_theme(app, refresh_notes_colors=load_saved_notes))
    btn_right_2.config(command=integrate_database)
    btn_right_3.config(command=export_pdf)

    delete_mode_on = False
    edit_mode_on = False

    def toggle_delete():
        nonlocal delete_mode_on, edit_mode_on
        delete_mode_on = not delete_mode_on
        if delete_mode_on:
            edit_mode_on = False
            btn_left_2.configure(bootstyle="danger")
            btn_left_3.configure(bootstyle="primary-outline")
        else:
            btn_left_2.configure(bootstyle="danger-outline")
        refresh_notes()

    from storage import set_editing, set_deleting

    def toggle_edit():
        nonlocal edit_mode_on, delete_mode_on
        edit_mode_on = not edit_mode_on
        set_editing(edit_mode_on)
        set_deleting(False)

        if edit_mode_on:
            delete_mode_on = False
            btn_left_3.configure(bootstyle="primary")
            btn_left_2.configure(bootstyle="danger-outline")
        else:
            btn_left_3.configure(bootstyle="primary-outline")

    btn_left_3.config(command=toggle_edit)