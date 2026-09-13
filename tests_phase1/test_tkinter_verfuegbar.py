"""Phase 1: tkinter/ttk ist Teil der Standardinstallation."""

import tkinter as tk
from tkinter import ttk


def test_tkinter_widgets() -> None:
    root = tk.Tk()
    root.withdraw()
    rahmen = ttk.LabelFrame(root, text="ECTS")
    label = ttk.Label(rahmen, text="0 %")
    balken = ttk.Progressbar(root, maximum=100)
    tabelle = ttk.Treeview(root, columns=("modul", "note"), show="headings")
    tabelle.heading("modul", text="Modul")
    tabelle.heading("note", text="Note")
    assert isinstance(rahmen, ttk.LabelFrame)
    assert isinstance(label, ttk.Label)
    assert isinstance(balken, ttk.Progressbar)
    assert isinstance(tabelle, ttk.Treeview)
    root.destroy()
    print("OK: tkinter/ttk ohne Zusatzpaket nutzbar")


if __name__ == "__main__":
    test_tkinter_widgets()
