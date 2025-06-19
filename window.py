import tkinter as tk
from storage import load_notes, is_deleting, is_editing
from actions import confirm_delete, open_note_editor, reset_modes


max_columns = 4
note_count = 0
notes_container = None
empty_label = None
app = None

def set_context(container, label, root):
    global notes_container, empty_label, app
    notes_container = container
    empty_label = label
    app = root

def display_note(note_data):
    global note_count
    row = note_count // max_columns
    column = max_columns - 1 - (note_count % max_columns)
    bg_color = note_data.get("Kolor", "#FFFFFF")

    note_frame = tk.Frame(notes_container, width=250, height=250, relief="raised", borderwidth=2, bg=bg_color, cursor="hand2")
    note_frame.grid(row=row, column=column, padx=10, pady=10)
    note_frame.pack_propagate(False)
    note_frame.configure(bg=bg_color)

    def on_enter(e): note_frame.config(relief="solid", borderwidth=3)
    def on_leave(e): note_frame.config(relief="raised", borderwidth=2)
    note_frame.bind("<Enter>", on_enter)
    note_frame.bind("<Leave>", on_leave)

    def open_note_info(note_data):
        info_win = tk.Toplevel(app)
        info_win.title(note_data.get("Tytuł", "Brak tytułu"))
        info_win.geometry("400x300")
        info_win.grab_set()

        tk.Label(info_win, text=note_data.get("Tytuł", ""), font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(info_win, text=f"Kategoria: {note_data.get('Kategoria', '')}", font=("Arial", 12, "italic")).pack(pady=5)
        tk.Label(info_win, text="Tagi:", font=("Arial", 12, "underline")).pack(anchor="w", padx=10)

        tags_frame = tk.Frame(info_win)
        tags_frame.pack(anchor="w", padx=10)
        for tag in note_data.get("Tagi", []):
            tk.Label(tags_frame, text=tag, borderwidth=1, relief="solid", padx=5, pady=2).pack(side="left", padx=2, pady=2)

        if "Zawartość" in note_data:
            content_text = tk.Text(info_win, wrap="word", height=10)
            content_text.pack(fill="both", expand=True, padx=10, pady=10)
            content_text.insert("1.0", note_data["Zawartość"])
            content_text.config(state="disabled")

    def on_click(e):
        if is_deleting():
            confirm_delete(note_data, load_saved_notes)
        elif is_editing():
            open_note_editor(note_data)
        else:
            open_note_info(note_data)
        reset_modes()
        load_saved_notes()

    note_frame.bind("<Button-1>", on_click)

    title_label = tk.Label(note_frame, text=note_data["Tytuł"], font=("Arial", 14, "bold"), wraplength=230, bg=bg_color)
    title_label.pack(pady=(10, 5))

    tags_frame = tk.Frame(note_frame, bg=bg_color)
    tags_frame.pack(pady=5)

    colors = ["#FF6666", "#66CC66", "#6699FF", "#FFCC33", "#3399FF", "#FF33AA"]
    for i, tag in enumerate(note_data["Tagi"]):
        color = colors[i % len(colors)]
        tag_label = tk.Label(tags_frame, text=tag, bg=color, padx=6, pady=2, borderwidth=1, relief="solid")
        tag_label.pack(side="left", padx=3)
    note_frame.custom_bg_color = bg_color

    category_label = tk.Label(note_frame, text=f"Kategoria: {note_data['Kategoria']}", font=("Arial", 10, "italic"), bg=bg_color)
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

        if (filter_text_lower in title or any(filter_text_lower in tag for tag in tags) or
                filter_text_lower in category or filter_text_lower in content):

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

def refresh_notes_colors():
    for note_frame in notes_container.winfo_children():
        bg_color = getattr(note_frame, "custom_bg_color", "#FFFFFF")
        note_frame.configure(bg=bg_color)
        for child in note_frame.winfo_children():
            try:
                child.configure(bg=bg_color)
            except:
                pass