import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Toplevel, Entry, Text, Button, Frame, Label
from tkinter import colorchooser
import datetime

last_id = 0
class NoteCreator(Toplevel):
    def __init__(self, parent, categories=None, on_save=None, note_data=None):
        super().__init__(parent)
        self.title("Notatka")
        self.geometry("1000x500")
        self.minsize(1400, 910)
        self.categories = categories if categories else []
        self.on_save = on_save
        self.tags = []
        self.note_data = note_data

        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        if self.note_data:
            self.load_note_data()

    def create_widgets(self):
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)

        left_frame = Frame(self)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        left_frame.columnconfigure(0, weight=1)

        Label(left_frame, text="Nazwa:", font=("Arial", 13, "bold")).grid(row=0, column=0, sticky="w")
        self.title_entry = Entry(left_frame, font=("Arial", 14))
        self.title_entry.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        Label(left_frame, text="Treść:", font=("Arial", 13, "bold")).grid(row=2, column=0, sticky="nw")
        self.text_entry = Text(left_frame, font=("Arial", 12))
        self.text_entry.grid(row=3, column=0, sticky="nsew")

        Label(left_frame, text="Kod PIN:", font=("Arial", 13, "bold")).grid(row=4, column=0, sticky="w")
        self.pin_entry = Entry(left_frame, show="*")
        self.pin_entry.grid(row=5, column=0, sticky="ew", pady=(0, 10))

        Label(left_frame, text="Data przypomnienia (RRRR-MM-DD):", font=("Arial", 13, "bold")).grid(row=6, column=0, sticky="w")
        self.reminder_entry = Entry(left_frame)
        self.reminder_entry.grid(row=7, column=0, sticky="ew", pady=(0, 10))

        Label(left_frame, text="Kolor:", font=("Arial", 13, "bold")).grid(row=8, column=0, sticky="w")
        self.color_btn = Button(left_frame, text="Wybierz kolor", command=self.choose_color)
        self.color_btn.grid(row=9, column=0, sticky="w")
        self.selected_color = "#FFFFFF"

        right_frame = Frame(self)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.add_tag_btn = Button(right_frame, text="Dodaj tag", command=self.add_tag_popup)
        self.add_tag_btn.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.tags_frame = Frame(right_frame)
        self.tags_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))

        Label(right_frame, text="Kategoria:", font=("Arial", 13, "bold")).grid(row=2, column=0, sticky="w")
        self.category_var = tk.StringVar()
        self.category_values = self.categories + ["Dodaj nową..."]
        self.category_combo = ttk.Combobox(right_frame, values=self.category_values, textvariable=self.category_var, state="readonly")
        self.category_combo.grid(row=3, column=0, sticky="ew")
        self.category_combo.current(0)
        self.category_combo.bind("<<ComboboxSelected>>", self.category_selected)

        self.ok_btn = Button(self, text="OK", command=self.save_note)
        self.ok_btn.grid(row=0, column=1, sticky="se", padx=10, pady=10)

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.selected_color = color
            self.color_btn.configure(style=f"{color}.TButton")

    def save_note(self):
        global last_id
        if self.note_data:
            note_id = self.note_data["id"]
        else:
            last_id += 1
            note_id = last_id

        note_data = {
            "id": note_id,
            "Tytuł": self.title_entry.get().strip(),
            "Zawartość": self.text_entry.get("1.0", "end-1c").strip(),
            "Kategoria": self.category_var.get(),
            "Tagi": self.tags,
            "KodPIN": self.pin_entry.get().strip(),
            "Przypomnienie": self.reminder_entry.get().strip(),
            "Kolor": self.selected_color,
            "created": self.note_data["created"] if self.note_data else datetime.datetime.now().strftime("%Y-%m-%d"),
            "modified": datetime.datetime.now().strftime("%Y-%m-%d")
        }
        if self.on_save:
            self.on_save(note_data)
        self.destroy()

    def add_tag_popup(self):
        popup = Toplevel(self)
        popup.title("Dodaj tag")
        popup.geometry("250x135")
        popup.transient(self)
        popup.grab_set()

        Label(popup, text="Tag:").pack(pady=5)
        tag_entry = Entry(popup)
        tag_entry.pack(pady=5)

        def add():
            tag = tag_entry.get().strip()
            if tag:
                self.tags.append(tag)
                lbl = tk.Label(self.tags_frame, text=tag, bg="lightgray", padx=5)
                lbl.pack(side="left", padx=5)

            popup.destroy()

        Button(popup, text="Dodaj", command=add).pack(pady=5)

        self.wait_window(popup)

    def category_selected(self, event):
        if self.category_var.get() == "Dodaj nową...":
            popup = Toplevel(self)
            popup.title("Nowa kategoria")
            popup.geometry("250x135")
            popup.transient(self)
            popup.grab_set()

            Label(popup, text="Nazwa kategorii:").pack(pady=5)
            entry = Entry(popup)
            entry.pack(pady=5)

            def add_category():
                new_cat = entry.get().strip()
                if new_cat and new_cat not in self.categories:
                    self.categories.append(new_cat)
                    self.category_values = self.categories + ["Dodaj nową..."]
                    self.category_combo["values"] = self.category_values
                    self.category_var.set(new_cat)
                popup.destroy()

            Button(popup, text="Dodaj", command=add_category).pack(pady=5)

            self.wait_window(popup)

    def load_note_data(self):
        self.title_entry.insert(0, self.note_data.get("Tytuł", ""))
        self.text_entry.insert("1.0", self.note_data.get("Zawartość", ""))
        self.category_var.set(self.note_data.get("Kategoria", ""))
        self.tags = self.note_data.get("Tagi", [])
        self.pin_entry.insert(0, self.note_data.get("KodPIN", ""))
        self.reminder_entry.insert(0, self.note_data.get("Przypomnienie", ""))
        self.selected_color = self.note_data.get("Kolor", "#FFFFFF")

    def close_window(self):
        self.destroy()

