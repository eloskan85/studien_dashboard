"""Anwendungsschicht: Die GUI spricht nur diese Klasse an."""

from __future__ import annotations

from datetime import date

from domain import (
    AmpelStatus,
    Belegung,
    Modul,
    ModulStatus,
    Pruefungsart,
    Semester,
    SemesterStatus,
    Student,
)
from persistenz import JsonRepository


class DashboardService:
    """Vermittelt zwischen Oberflaeche und Fachlogik. Rechnet selbst nicht."""

    def __init__(self, repository: JsonRepository) -> None:
        self.repository = repository
        self.student: Student | None = None

    def lade_daten(self) -> Student:
        """Laedt den Student aus der JSON-Datei."""
        self.student = self.repository.laden()
        self._semester_auffuellen()
        return self.student

    def _semester_auffuellen(self) -> None:
        """Legt fehlende Semester 1 bis max_semester an."""
        sg = self.student.studiengang
        vorhanden = {s.nummer for s in sg.semester}
        for nummer in range(1, sg.max_semester + 1):
            if nummer not in vorhanden:
                sg.semester.append(
                    Semester(nummer, f"Semester {nummer}", SemesterStatus.GEPLANT)
                )
        sg.semester.sort(key=lambda s: s.nummer)

    def _naechste_modul_id(self) -> str:
        """Vergibt intern die naechste freie ID (M1, M2, ...)."""
        nummern = []
        for m in self.student.studiengang.module:
            rest = m.modul_id[1:] if m.modul_id.startswith("M") else ""
            if rest.isdigit():
                nummern.append(int(rest))
        return f"M{max(nummern, default=0) + 1}"

    def neues_modul(
        self,
        name: str,
        ects_text: str,
        semester_name: str,
        status: str,
    ) -> None:
        """Legt Modul und Belegung an. Die ID vergibt der Service."""
        name = name.strip()
        if not name:
            raise ValueError("Name ist nötig.")
        ects = int(ects_text.strip())
        modul = Modul(self._naechste_modul_id(), name, ects)
        self.student.studiengang.module.append(modul)
        belegung = Belegung(modul, ModulStatus[status])
        if semester_name:
            belegung.semester = next(
                (s for s in self.student.studiengang.semester if s.bezeichnung == semester_name),
                None,
            )
        self.student.belegungen.append(belegung)

    def ects_fortschritt(self) -> float:
        """Anteil bestandener ECTS in Prozent. Der Student berechnet den Wert."""
        return self.student.berechne_ects_fortschritt()

    def notendurchschnitt(self) -> float:
        """Gewichteter Schnitt. Der Student berechnet den Wert."""
        return self.student.berechne_notendurchschnitt()

    def zeitfortschritt(self) -> float:
        """Zeitanteil aus studienbeginn. Der Student berechnet den Wert."""
        return self.student.berechne_zeitfortschritt()

    def ampel(self) -> AmpelStatus:
        """Zielampel. Der Student berechnet den Wert."""
        return self.student.ermittle_ziel_ampel()

    def speichere_belegung(
        self,
        belegung: Belegung,
        status: str,
        note_text: str,
        semester_name: str,
        art: str | None = None,
    ) -> None:
        """Uebernimmt Dialogwerte in die Belegung. Speichert noch nicht."""
        belegung.status = ModulStatus[status]
        if semester_name:
            gefunden = next(
                (s for s in self.student.studiengang.semester if s.bezeichnung == semester_name),
                None,
            )
            belegung.semester = gefunden
        if status in ("GEPLANT", "BELEGT"):
            belegung.pruefungsleistung = None
            return
        note_text = note_text.strip().replace(",", ".")
        if note_text:
            note = float(note_text)
            art_enum = Pruefungsart[art] if art else (
                belegung.pruefungsleistung.art if belegung.pruefungsleistung else Pruefungsart.KLAUSUR
            )
            belegung.setze_note(note, art_enum, date.today())

    def loesche_modul(self, modul_id: str) -> None:
        """Entfernt Belegung und Modul."""
        self.student.belegungen = [
            b for b in self.student.belegungen if b.modul.modul_id != modul_id
        ]
        self.student.studiengang.module = [
            m for m in self.student.studiengang.module if m.modul_id != modul_id
        ]

    def speichern(self) -> None:
        """Schreibt den aktuellen Student über das Repository nach JSON."""
        self.repository.speichern(self.student)