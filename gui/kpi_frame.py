"""KPI-Kacheln. Zeigen nur Werte, rechnen nicht."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


AMPEL_TEXT = {
    "GRUEN": ("Ziel sicher", "#2e7d32"),
    "GELB": ("Ziel gefährdet", "#c77700"),
    "ROT": ("Ziel verfehlt", "#c62828"),
}

KANTEN = ("#1a5276", "#2e7d32", "#c77700", "#c9a227")


class KpiFrame(ttk.Frame):
    """Verantwortlich für die Anzeige von ECTS, Note, Zeit und Ampel."""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.werte: dict[str, tk.Label] = {}
        self.unter: dict[str, tk.Label] = {}
        titel = (
            ("ects", "ECTS-FORTSCHRITT"),
            ("note", "NOTENDURCHSCHNITT"),
            ("zeit", "ZEITFORTSCHRITT"),
            ("ampel", "ZIEL-AMPEL"),
        )
        for i, (key, name) in enumerate(titel):
            self.columnconfigure(i, weight=1)
            kachel = tk.Frame(self, bg="white", highlightbackground="#d0d7de", highlightthickness=1)
            kachel.grid(row=0, column=i, padx=8, pady=6, sticky="nsew")
            tk.Frame(kachel, bg=KANTEN[i], height=4).pack(fill="x")
            tk.Label(kachel, text=name, bg="white", fg="#5d6d7e", font=("Arial", 8)).pack(
                anchor="w", padx=12, pady=(10, 0)
            )
            wert = tk.Label(kachel, text="–", bg="white", fg="#1a252f", font=("Arial", 20, "bold"))
            wert.pack(anchor="w", padx=12, pady=(2, 0))
            unter = tk.Label(kachel, text="", bg="white", fg="#7f8c8d", font=("Arial", 9))
            unter.pack(anchor="w", padx=12, pady=(0, 12))
            self.werte[key] = wert
            self.unter[key] = unter

    def aktualisieren(
        self,
        ects: float,
        note: float,
        zeit: float,
        ampel: str,
        erreicht: int = 0,
        gesamt: int = 180,
        fachsemester: int = 1,
        max_semester: int = 8,
    ) -> None:
        """Setzt Anzeigetexte. ampel ist der Enum-Name GRUEN/GELB/ROT."""
        self.werte["ects"].config(text=f"{erreicht} / {gesamt}")
        self.unter["ects"].config(text=f"{ects:.0f} % erreicht")
        self.werte["note"].config(text=f"{note:.2f}".replace(".", ",") if note else "–")
        self.unter["note"].config(text="Soll unter 2,0")
        self.werte["zeit"].config(text=f"Sem. {fachsemester}/{max_semester}")
        self.unter["zeit"].config(text=f"{zeit:.0f} % der Studienzeit")
        text, farbe = AMPEL_TEXT.get(ampel, (ampel, "#123"))
        self.werte["ampel"].config(text=text, fg=farbe)
        self.unter["ampel"].config(text=ampel)