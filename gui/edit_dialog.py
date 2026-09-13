"""Dialog zum Anlegen und Bearbeiten einer Belegung."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from domain import Belegung, Pruefungsart
from domain.model import ERLAUBTE_NOTEN


class EditDialog(tk.Toplevel):
    """Erfasst Moduldaten, Status, Note, Art und Semester. Speichert nicht selbst."""

    def __init__(
        self,
        parent,
        semester_liste: list[str],
        on_save,
        belegung: Belegung | None = None,
    ) -> None:
        super().__init__(parent)
        self.on_save = on_save
        self.belegung = belegung
        self.neu = belegung is None
        self.title("Modul anlegen" if self.neu else "Belegung bearbeiten")
        self.resizable(False, False)

        row = 0
        self.name = None
        self.ects = None

        if self.neu:
            ttk.Label(self, text="Name").grid(row=row, column=0, sticky="w", padx=10, pady=6)
            self.name = ttk.Entry(self, width=30)
            self.name.grid(row=row, column=1, padx=10, pady=6)
            row += 1
            ttk.Label(self, text="ECTS").grid(row=row, column=0, sticky="w", padx=10, pady=6)
            self.ects = ttk.Entry(self, width=30)
            self.ects.insert(0, "5")
            self.ects.grid(row=row, column=1, padx=10, pady=6)
            row += 1
        else:
            ttk.Label(self, text=belegung.modul.name).grid(
                row=row, column=0, columnspan=2, pady=(12, 8)
            )
            row += 1

        ttk.Label(self, text="Status").grid(row=row, column=0, sticky="w", padx=10, pady=6)
        self.status = ttk.Combobox(
            self,
            values=["GEPLANT", "BELEGT", "BESTANDEN", "NICHT_BESTANDEN"],
            state="readonly",
            width=28,
        )
        self.status.set(belegung.status.name if belegung else "GEPLANT")
        self.status.grid(row=row, column=1, padx=10, pady=6)
        self.status.bind("<<ComboboxSelected>>", lambda _e: self._note_sichtbar())
        row += 1

        self.lbl_note = ttk.Label(self, text="Note")
        self.lbl_note.grid(row=row, column=0, sticky="w", padx=10, pady=6)
        noten = [f"{n:.1f}".replace(".", ",") for n in ERLAUBTE_NOTEN]
        self.note = ttk.Combobox(self, values=noten, state="readonly", width=28)
        if belegung and belegung.pruefungsleistung:
            self.note.set(f"{belegung.pruefungsleistung.note:.1f}".replace(".", ","))
        self.note.grid(row=row, column=1, padx=10, pady=6)
        row += 1

        ttk.Label(self, text="Prüfungsart").grid(row=row, column=0, sticky="w", padx=10, pady=6)
        self.art = ttk.Combobox(self, values=[a.name for a in Pruefungsart], state="readonly", width=28)
        if belegung and belegung.pruefungsleistung:
            self.art.set(belegung.pruefungsleistung.art.name)
        else:
            self.art.set("KLAUSUR")
        self.art.grid(row=row, column=1, padx=10, pady=6)
        row += 1

        ttk.Label(self, text="Semester").grid(row=row, column=0, sticky="w", padx=10, pady=6)
        self.semester = ttk.Combobox(self, values=semester_liste, state="readonly", width=28)
        if belegung and belegung.semester:
            self.semester.set(belegung.semester.bezeichnung)
        elif semester_liste:
            self.semester.set(semester_liste[0])
        self.semester.grid(row=row, column=1, padx=10, pady=6)
        row += 1

        ttk.Button(self, text="Speichern", command=self.speichern).grid(
            row=row, column=0, columnspan=2, pady=14
        )
        self._note_sichtbar()
        self.transient(parent)
        self.grab_set()

    def _note_sichtbar(self) -> None:
        """Note nur bei BESTANDEN und NICHT_BESTANDEN."""
        if self.status.get() in ("BESTANDEN", "NICHT_BESTANDEN"):
            self.lbl_note.grid()
            self.note.grid()
        else:
            self.note.set("")
            self.lbl_note.grid_remove()
            self.note.grid_remove()

    def speichern(self) -> None:
        """Gibt die Eingaben zurueck und schließt den Dialog."""
        try:
            if self.neu:
                self.on_save(
                    self.name.get(),
                    self.ects.get(),
                    self.status.get(),
                    self.note.get(),
                    self.art.get(),
                    self.semester.get(),
                )
            else:
                self.on_save(
                    self.status.get(),
                    self.note.get(),
                    self.semester.get(),
                    self.art.get(),
                )
        except ValueError as fehler:
            messagebox.showerror(self.title(), str(fehler), parent=self)
            return
        self.destroy()