"""Hauptfenster. Kennt den Service, nicht das Repository."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from anwendung.dashboard_service import DashboardService
from gui.edit_dialog import EditDialog
from gui.kpi_frame import KpiFrame
from gui.module_table import ModuleTable


class DashboardApp:
    """Koordiniert Kopfzeile, KPI-Kacheln, Balken, Tabelle und Dialog."""

    def __init__(self, service: DashboardService) -> None:
        self.service = service
        self.root = tk.Tk()
        self.root.title("Studien-Dashboard")
        self.root.geometry("1000x680")
        self.root.configure(bg="#f4f7fb")
        self.aufbauen_gui()
        self.aktualisieren()

    def aufbauen_gui(self) -> None:
        """Erzeugt Kopfzeile, Kacheln, Balken und Tabelle."""
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        kopf = tk.Frame(self.root, bg="#1a5276")
        kopf.pack(fill="x")
        self.lbl_kopf = tk.Label(
            kopf, text="", bg="#1a5276", fg="white", font=("Arial", 13, "bold"), pady=12
        )
        self.lbl_kopf.pack(anchor="w", padx=16)
        self.lbl_beginn = tk.Label(kopf, text="", bg="#1a5276", fg="#d6eaf8", font=("Arial", 10))
        self.lbl_beginn.pack(anchor="w", padx=16, pady=(0, 10))

        self.kpi = KpiFrame(self.root)
        self.kpi.pack(fill="x", padx=8, pady=(8, 0))

        balken_box = ttk.Frame(self.root)
        balken_box.pack(fill="x", padx=16, pady=8)
        balken_kopf = ttk.Frame(balken_box)
        balken_kopf.pack(fill="x")
        ttk.Label(balken_kopf, text="Gesamtfortschritt Studium").pack(side="left")
        self.lbl_balken = ttk.Label(balken_kopf, text="")
        self.lbl_balken.pack(side="right")
        self.balken = ttk.Progressbar(balken_box, maximum=100, length=400)
        self.balken.pack(fill="x", pady=4)

        zeile = ttk.Frame(self.root)
        zeile.pack(fill="x", padx=16)
        ttk.Label(zeile, text="Module  (Doppelklick zum Bearbeiten)").pack(side="left")
        ttk.Button(zeile, text="Löschen", command=self.loesche_modul).pack(side="right", padx=(0, 8))
        ttk.Button(zeile, text="+ Modul", command=self.oeffne_neu_modul).pack(side="right")
        self.tabelle = ModuleTable(self.root, on_edit=self.oeffne_edit_dialog)
        self.tabelle.pack(fill="both", expand=True, padx=16, pady=(4, 16))

    def aktualisieren(self) -> None:
        """Holt Kennzahlen vom Service und fuellt Kacheln sowie Tabelle."""
        s = self.service.student
        self.lbl_kopf.config(
            text=f"{s.studiengang.name}   |   {s.vorname} {s.nachname}   |   {s.matrikelnummer}"
        )
        self.lbl_beginn.config(
            text=f"Studienbeginn: {s.studienbeginn.isoformat()}   |   max. {s.studiengang.max_semester} Semester"
        )
        ects = self.service.ects_fortschritt()
        note = self.service.notendurchschnitt()
        zeit = self.service.zeitfortschritt()
        erreicht = sum(b.modul.ects for b in s.belegungen if b.ist_bestanden)
        gesamt = s.studiengang.gesamtects
        max_sem = s.studiengang.max_semester
        fachsemester = max(1, min(max_sem, round(zeit / 100 * max_sem) or 1))
        self.kpi.aktualisieren(
            ects,
            note,
            zeit,
            self.service.ampel().name,
            erreicht,
            gesamt,
            fachsemester,
            max_sem,
        )
        self.balken["value"] = ects
        self.lbl_balken.config(text=f"{erreicht} von {gesamt} ECTS  ·  {ects:.0f} %")

        zeilen = []
        for b in s.belegungen:
            pl = b.pruefungsleistung
            zeilen.append({
                "id": b.modul.modul_id,
                "modul": b.modul.name,
                "semester": b.semester.bezeichnung if b.semester else "–",
                "ects": b.modul.ects,
                "status": b.status.name,
                "note": f"{pl.note:.1f}".replace(".", ",") if pl else "–",
                "art": pl.art.name if pl else "–",
            })
        self.tabelle.laden(zeilen)

    def oeffne_edit_dialog(self) -> None:
        """Oeffnet den Dialog zur gewaehlten Belegung und speichert über den Service."""
        mid = self.tabelle.gewaehlte_id()
        if not mid:
            return
        belegung = next(b for b in self.service.student.belegungen if b.modul.modul_id == mid)
        semester = [sem.bezeichnung for sem in self.service.student.studiengang.semester]

        def speichern(status, note, sem_name, art):
            self.service.speichere_belegung(belegung, status, note, sem_name, art)
            self.service.speichern()
            self.aktualisieren()

        EditDialog(self.root, semester, speichern, belegung=belegung)

    def loesche_modul(self) -> None:
        """Loescht die markierte Belegung nach Rueckfrage."""
        mid = self.tabelle.gewaehlte_id()
        if not mid:
            messagebox.showinfo("Löschen", "Bitte zuerst eine Zeile markieren.")
            return
        name = next(b.modul.name for b in self.service.student.belegungen if b.modul.modul_id == mid)
        if not messagebox.askyesno("Löschen", f"Modul „{name}“ wirklich löschen?"):
            return
        self.service.loesche_modul(mid)
        self.service.speichern()
        self.aktualisieren()

    def oeffne_neu_modul(self) -> None:
        """Oeffnet denselben Dialog ohne Belegung, also zum Anlegen."""
        semester = [sem.bezeichnung for sem in self.service.student.studiengang.semester]

        def anlegen(name, ects_text, status, note, art, sem_name):
            self.service.neues_modul(name, ects_text, sem_name, status)
            belegung = self.service.student.belegungen[-1]
            self.service.speichere_belegung(belegung, status, note, sem_name, art)
            self.service.speichern()
            self.aktualisieren()

        EditDialog(self.root, semester, anlegen, belegung=None)

    def start(self) -> None:
        """Startet die tkinter-Ereignisschleife/Oberflaeche."""
        self.root.mainloop()