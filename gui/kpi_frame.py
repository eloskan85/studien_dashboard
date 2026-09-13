"""KPI-Kacheln. Zeigen nur Werte, rechnen nicht."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


FARBE = {
    "GRUEN": "#2e7d32",
    "GELB": "#f9a825",
    "ROT": "#c62828",
}


class KpiFrame(ttk.Frame):
    """Verantwortlich für die Anzeige von ECTS, Note, Zeit und Ampel."""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.werte: dict[str, tk.Label] = {}
        titel = (
            ("ects", "ECTS-Fortschritt"),
            ("note", "Note (Soll < 2,0)"),
            ("zeit", "Zeitfortschritt"),
            ("ampel", "Ziel-Ampel"),
        )
        for i, (key, name) in enumerate(titel):
            self.columnconfigure(i, weight=1)
            kachel = tk.Frame(self, bg="#e8f4fd", highlightbackground="#1a5276", highlightthickness=1)
            kachel.grid(row=0, column=i, padx=8, pady=6, sticky="nsew")
            tk.Label(kachel, text=name, bg="#e8f4fd", fg="#1a5276", font=("Arial", 10)).pack(pady=(10, 2))
            wert = tk.Label(kachel, text="–", bg="#e8f4fd", fg="#123", font=("Arial", 18, "bold"))
            wert.pack(pady=(0, 12))
            self.werte[key] = wert

    def aktualisieren(self, ects: float, note: float, zeit: float, ampel: str) -> None:
        """Setzt die Anzeigetexte. ampel ist der Enum-Name GRUEN/GELB/ROT."""
        self.werte["ects"].config(text=f"{ects:.0f} %")
        self.werte["note"].config(text=f"{note:.2f}" if note else "–")
        self.werte["zeit"].config(text=f"{zeit:.0f} %")
        self.werte["ampel"].config(text=ampel, fg=FARBE.get(ampel, "#123"))
