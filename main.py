from ttkbootstrap import Window
from ui import build_interface
from window import load_saved_notes

def main():
    app = Window(themename="vapor")
    app.title("Notatnik")
    app.geometry("900x600")
    app.minsize(700, 500)

    build_interface(app)
    load_saved_notes()

    app.mainloop()

if __name__ == "__main__":
    main()