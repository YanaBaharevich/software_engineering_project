import tkinter as tk
import json
import os
from storage import load_notes, is_deleting, is_editing, set_deleting, set_editing
from note_creator import NoteCreator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from tkinter import filedialog, messagebox
import textwrap
import pyodbc
from datetime import datetime

def toggle_delete_mode(refresh_callback=None):
    if is_editing():
        set_editing(False)
    set_deleting(not is_deleting())
    if refresh_callback:
        refresh_callback()

def toggle_edit_mode(window):
    window.set_mode("edit")
    window.set_status("Wybierz notatkę do edycji")


def confirm_delete(note_data, refresh_notes_callback):
    confirm_win = tk.Toplevel()
    confirm_win.title("Potwierdzenie usunięcia")
    confirm_win.geometry("300x150")
    confirm_win.grab_set()

    def on_close():
        refresh_notes_callback()
        reset_modes()
        confirm_win.destroy()

    confirm_win.protocol("WM_DELETE_WINDOW", on_close)

    def delete_and_close():
        remove_note(note_data)
        refresh_notes_callback()
        reset_modes()
        confirm_win.destroy()

    tk.Label(confirm_win, text=f"Usunąć notatkę: {note_data['Tytuł']}?", font=("Arial", 11)).pack(pady=10)
    tk.Button(confirm_win, text="Tak", command=delete_and_close).pack(side="left", padx=20, pady=10)
    tk.Button(confirm_win, text="Nie", command=on_close).pack(side="right", padx=20, pady=10)


def remove_note(note_data):
    notes = load_notes()
    notes = [note for note in notes if note.get("id") != note_data.get("id")]
    with open("saved_notes.json", "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=4)

def reset_modes():
    set_deleting(False)
    set_editing(False)

def open_note_editor(note_data):
    def on_save_edited_note(updated_note_data):
        notes = load_notes()
        for i, note in enumerate(notes):
            if note.get("id") == updated_note_data.get("id"):
                notes[i] = updated_note_data
                break
        with open("saved_notes.json", "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=4)
        reset_modes()

    NoteCreator(
        None,
        categories=["Praca", "Osobiste", "Nauka"],
        on_save=on_save_edited_note,
        note_data=note_data
    ).grab_set()


def toggle_theme(app, refresh_notes_colors):
    current_theme = app.style.theme_use()
    new_theme = "vapor" if current_theme != "vapor" else "morph"
    app.style.theme_use(new_theme)
    refresh_notes_colors()

def integrate_database():
    try:
        conn = pyodbc.connect(
            "Driver={SQL Server};"
            "Server=DESKTOP-A6AIHCM;"
            "Database=zajęcia;"
            "Trusted_Connection=yes;"
        )
        cursor = conn.cursor()

        notes = load_notes()

        for note in notes:
            tytul = note.get("Tytuł", "")
            zawartosc = note.get("Zawartość", "")
            pin = note.get("KodPIN")
            if not pin or str(pin).strip() == "":
                pin = None

            data_raw = note.get("Przypomnienie")
            data_przyp = None
            if data_raw:
                try:
                    data_przyp = datetime.strptime(data_raw, "%Y-%m-%d")
                except ValueError:
                    try:
                        data_przyp = datetime.fromisoformat(data_raw)
                    except ValueError:
                        data_przyp = None
            kolor = note.get("Kolor", "#FFFFFF")  # domyślnie biały, jeśli brak
            kategoria = note.get("Kategoria", "")
            tagi = ", ".join(note.get("Tagi", []))

            cursor.execute("""
                INSERT INTO Notatki (Tytul, Zawartosc, KodPIN, DataPrzypomnienia, Kolor)
                VALUES (?, ?, ?, ?, ?)
            """, (tytul, zawartosc, pin, data_przyp, kolor))

            cursor.execute("""
                INSERT INTO Identyfikatory (Tytul, Kategoria, Tagi)
                VALUES (?, ?, ?)
            """, (tytul, kategoria, tagi))

        conn.commit()
        messagebox.showinfo("Sukces", "Notatki zapisane do bazy danych.")
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas zapisu do bazy: {str(e)}")


def export_pdf():
    notes = load_notes()
    if not notes:
        messagebox.showinfo("Brak danych", "Brak notatek do eksportu.")
        return

    font_path = "DejaVuSans.ttf"
    if not os.path.exists(font_path):
        messagebox.showerror("Błąd", f"Plik czcionki {font_path} nie został znaleziony. Umieść go w katalogu z aplikacją.")
        return

    pdfmetrics.registerFont(TTFont("DejaVu", font_path))

    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return

    try:
        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
        y = height - 50

        for note in notes:
            c.setFont("DejaVu", 14)
            c.drawString(50, y, f"Tytuł: {note.get('Tytuł', '')}")
            y -= 20

            c.setFont("DejaVu", 12)
            c.drawString(50, y, f"Kategoria: {note.get('Kategoria', '')}")
            y -= 20

            tags = ", ".join(note.get("Tagi", []))
            c.drawString(50, y, f"Tagi: {tags}")
            y -= 20

            c.drawString(50, y, "Treść:")
            y -= 15

            content_lines = note.get("Zawartość", "").split("\n")
            for line in content_lines:
                wrapped_lines = textwrap.wrap(line, width=80)
                for wrapped_line in wrapped_lines:
                    if y < 50:
                        c.showPage()
                        c.setFont("DejaVu", 12)
                        y = height - 50
                    c.drawString(60, y, wrapped_line)
                    y -= 15

            y -= 30

        c.save()
        messagebox.showinfo("Sukces", f"Notatki wyeksportowane do {file_path}")

    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się zapisać pliku PDF: {str(e)}")