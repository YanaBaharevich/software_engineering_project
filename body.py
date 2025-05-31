import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

app = tb.Window(themename="vapor")
app.title("Notatnik")
app.geometry("900x600")
app.minsize(700, 500)

app.rowconfigure(0, weight=0)     # Zona przycisków
app.columnconfigure(0, weight=3)  # Lewa
app.columnconfigure(1, weight=1)  # Prawa
app.rowconfigure(1, weight=0)
app.rowconfigure(2, weight=1)     # Zona notatek

top_frame = tk.Frame(app)
top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
top_frame.columnconfigure(0, weight=3)
top_frame.columnconfigure(1, weight=1)

left_buttons_frame = tb.Frame(top_frame)
left_buttons_frame.grid(row=0, column=0, sticky="w")

btn_left_1 = ttk.Button(left_buttons_frame, text="Dodaj notatkę", bootstyle="success-outline")
btn_left_2 = ttk.Button(left_buttons_frame, text="Usuń notatkę", bootstyle="danger-outline")
btn_left_3 = ttk.Button(left_buttons_frame, text="Edytuj notatkę", bootstyle="primary-outline")
btn_left_1.pack(side="left", padx=5)
btn_left_2.pack(side="left", padx=5)
btn_left_3.pack(side="left", padx=5)

right_buttons_frame = tb.Frame(top_frame)
right_buttons_frame.grid(row=0, column=1, sticky="e")

btn_right_1 = ttk.Button(right_buttons_frame, text="Zmień tryb na jasny/ciemny", bootstyle="info-outline")
btn_right_2 = ttk.Button(right_buttons_frame, text="Zintegruj z kalendarzem", bootstyle="primary-outline")

btn_right_1.pack(side="top", fill="x", pady=5)
btn_right_2.pack(side="top", fill="x", pady=5)

separator = ttk.Separator(app, orient='horizontal')
separator.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10)

notes_frame = tb.Frame(app)
notes_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

app.rowconfigure(2, weight=1)
app.columnconfigure(0, weight=3)
app.columnconfigure(1, weight=1)
notes_frame.rowconfigure(0, weight=1)
notes_frame.columnconfigure(0, weight=1)

