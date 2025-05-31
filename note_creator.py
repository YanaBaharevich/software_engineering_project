import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from ttkbootstrap import Toplevel, Entry, Text, Button, Frame, Label, Combobox



class NoteCreator(Toplevel):
    def __init__(self, parent, categories=None, on_save=None):
        super().__init__(parent)
        self.title("Notatka")
        self.geometry("1000x400")
        self.minsize(400, 300)
        self.categories = categories if categories else []
        self.on_save = on_save  # callback для передачи данных в главное окно
        self.tags = []
        self.tags_frame = Frame(self)
        self.tags_frame.grid(row=4, column=0, sticky="ew", pady=(10, 0))

        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def create_widgets(self):
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        left_frame = Frame(self)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(2, weight=1)

        Label(left_frame, text="Nazwa:", font=("Arial", 13, "bold")).grid(row=0, column=0, sticky="w")
        self.title_entry = Entry(left_frame, font=("Arial", 14))
        self.title_entry.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        Label(left_frame, text="Treść:", font=("Arial", 13, "bold")).grid(row=2, column=0, sticky="nw")
        self.text_entry = Text(left_frame, font=("Arial", 12))
        self.text_entry.grid(row=3, column=0, sticky="nsew")

        right_frame = Frame(self)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        right_frame.columnconfigure(0, weight=1)

        self.add_tag_btn = Button(right_frame, text="Dodaj tag", command=self.add_tag_popup)
        self.add_tag_btn.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.tags_frame = Frame(right_frame)
        self.tags_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))

        Label(right_frame, text="Kategoria:", font=("Arial", 13, "bold")).grid(row=2, column=0, sticky="w")

        self.category_values = self.categories + ["Dodaj nową..."]
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(right_frame, values=self.category_values, textvariable=self.category_var, state="readonly")
        self.category_combo.grid(row=3, column=0, sticky="ew")
        self.category_combo.current(0)
        self.category_combo.bind("<<ComboboxSelected>>", self.category_selected)

        self.ok_btn = Button(self, text="OK", command=self.save_note)
        self.ok_btn.grid(row=1, column=1, sticky="e", padx=10, pady=10)

    def category_selected(self, event):
        if self.category_var.get() == "Dodaj nową...":
            self.add_category_popup()

    def add_category_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Dodaj kategorię")
        popup.geometry("250x100")
        popup.grab_set()

        tk.Label(popup, text="Nazwa kategorii:").pack(pady=5)
        category_entry = tk.Entry(popup)
        category_entry.pack(pady=5, fill="x", padx=10)

        def save_category():
            category = category_entry.get().strip()
            if category and category not in self.categories:
                self.categories.append(category)
                self.category_values = self.categories + ["Dodaj nową..."]
                self.category_combo['values'] = self.category_values
                self.category_var.set(category)
            popup.destroy()

        tk.Button(popup, text="Dodaj", command=save_category).pack(pady=5)

    def add_tag_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Dodaj tag")
        popup.geometry("250x100")
        popup.grab_set()

        tk.Label(popup, text="Nazwa taga:").pack(pady=5)
        tag_entry = tk.Entry(popup)
        tag_entry.pack(pady=5, fill="x", padx=10)

        def save_tag():
            tag = tag_entry.get().strip()
            if tag and tag not in self.tags:
                self.tags.append(tag)
                colors = ["#FF9999", "#99FF99", "#9999FF", "#FFCC66", "#66CCFF", "#FF66CC"]
                color = colors[len(self.tags) % len(colors)]
                tag_label = tk.Label(
                    self.tags_frame,
                    text=tag,
                    bg=color,
                    fg="black",
                    padx=5,
                    pady=2,
                    borderwidth=1,
                    relief="solid"
                )
                tag_label.pack(side="left", padx=3)
            popup.destroy()

        tk.Button(popup, text="Dodaj", command=save_tag).pack(pady=5)

    def display_tags(self):
        for widget in self.tags_frame.winfo_children():
            widget.destroy()

        colors = ["#FF6666", "#66CC66", "#6699FF", "#FFCC33", "#3399FF", "#FF33AA"]
        for i, tag in enumerate(self.tags):
            color = colors[i % len(colors)]
            tag_label = tk.Label(
                self.tags_frame,
                text=tag,
                bg=color,
                fg="black",
                font=("Arial", 14, "bold"),
                padx=10,
                pady=5,
                borderwidth=1,
                relief="solid"
            )
            tag_label.pack(side="left", padx=5)

    def save_note(self):
        title = self.title_entry.get().strip()
        text = self.text_entry.get("1.0", "end-1c").strip()
        category = self.category_var.get()
        tags = self.tags.copy()

        if category == "Add a new one...":
            category = None

        if self.on_save:
            self.on_save({
                "title": title,
                "text": text,
                "category": category,
                "tags": tags
            })
        self.destroy()

    def close_window(self):
        self.destroy()
