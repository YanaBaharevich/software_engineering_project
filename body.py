import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

default_bg = "#e4c0a8"
app = ThemedTk(theme="radiance")
main_frame = tk.Frame(app, bg=default_bg)

app.configure(bg=default_bg)
main_frame.pack(fill="both", expand=True)

app.title("Notanik")
app.geometry("700x500")

app.mainloop()
