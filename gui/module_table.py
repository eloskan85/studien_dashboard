"""Modultabelle. Kein Dateizugriff, keine Berechnung."""

from __future__ import annotations

from tkinter import ttk


class ModuleTable(ttk.Frame):
    """Verantwortlich für die Uebersicht der Belegungen. Doppelklick oeffnet den Bearbeiten-Dialog."""

    def __init__(self, parent, on_edit) -> None:
        super().__init__(parent)
        self.on_edit = on_edit
        spalten = ("modul", "semester", "ects", "status", "note", "art")
        koepfe = ("Modul", "Semester", "ECTS", "Status", "Note", "Art")
        self.tree = ttk.Treeview(self, columns=spalten, show="headings", height=12)
        for sp, k in zip(spalten, koepfe):
            self.tree.heading(sp, text=k)
            self.tree.column(sp, width=120, anchor="center")
        self.tree.column("modul", width=220, anchor="w")
        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.tree.bind("<Double-1>", lambda _e: on_edit())

    def laden(self, zeilen: list[dict]) -> None:
        """Fuellt die Tabelle. id ist die modul_id."""
        self.tree.delete(*self.tree.get_children())
        for z in zeilen:
            self.tree.insert("", "end", iid=z["id"], values=(
                z["modul"], z["semester"], z["ects"], z["status"], z["note"], z["art"]
            ))

    def gewaehlte_id(self) -> str | None:
        """Modul-ID der markierten Zeile oder None."""
        auswahl = self.tree.selection()
        return auswahl[0] if auswahl else None
