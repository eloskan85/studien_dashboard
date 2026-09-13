"""Persistenz ueber eine lokale JSON-Datei. Keine fachliche Berechnung."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from domain import (
    Belegung,
    Modul,
    ModulStatus,
    Pruefungsart,
    Pruefungsleistung,
    Semester,
    SemesterStatus,
    Student,
    Studiengang,
)


class JsonRepository:
    """Speichert und laedt den Student als JSON.

    Enums und Datumsangaben werden als Text geschrieben und beim Laden
    wieder in Domain-Typen gewandelt. Optionale Felder bleiben None.
    """

    def __init__(self, dateipfad: str) -> None:
        self.dateipfad = dateipfad

    def laden(self) -> Student:
        """Liest die Datei und baut den Objektgraphen auf."""
        roh = json.loads(Path(self.dateipfad).read_text(encoding="utf-8"))
        return self._from_dict(roh)

    def speichern(self, student: Student) -> None:
        """Schreibt den Student inkl. Belegungen nach dateipfad."""
        Path(self.dateipfad).write_text(
            json.dumps(self._to_dict(student), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def _to_dict(self, student: Student) -> dict:
        """Wandelt Domain-Objekte in JSON-faehige Dictionaries."""
        sg = student.studiengang
        return {
            "matrikelnummer": student.matrikelnummer,
            "vorname": student.vorname,
            "nachname": student.nachname,
            "studienbeginn": student.studienbeginn.isoformat(),
            "studiengang": {
                "name": sg.name,
                "gesamtects": sg.gesamtects,
                "max_semester": sg.max_semester,
                "semester": [
                    {
                        "nummer": s.nummer,
                        "bezeichnung": s.bezeichnung,
                        "status": s.status.name,
                    }
                    for s in sg.semester
                ],
                "module": [
                    {"modul_id": m.modul_id, "name": m.name, "ects": m.ects}
                    for m in sg.module
                ],
            },
            "belegungen": [
                {
                    "modul_id": b.modul.modul_id,
                    "status": b.status.name,
                    "semester_nummer": b.semester.nummer if b.semester else None,
                    "pruefungsleistung": None
                    if b.pruefungsleistung is None
                    else {
                        "art": b.pruefungsleistung.art.name,
                        "note": b.pruefungsleistung.note,
                        "datum": b.pruefungsleistung.datum.isoformat(),
                        "seitenumfang": b.pruefungsleistung.seitenumfang,
                        "dauer_minuten": b.pruefungsleistung.dauer_minuten,
                    },
                }
                for b in student.belegungen
            ],
        }

    def _from_dict(self, data: dict) -> Student:
        """Baut Student, Studiengang, Module und Belegungen aus JSON."""
        sg_roh = data["studiengang"]
        sg = Studiengang(sg_roh["name"], sg_roh["gesamtects"], sg_roh["max_semester"])
        for s in sg_roh.get("semester", []):
            sg.semester.append(
                Semester(s["nummer"], s["bezeichnung"], SemesterStatus[s["status"]])
            )
        module = {}
        for m in sg_roh.get("module", []):
            modul = Modul(m["modul_id"], m["name"], m["ects"])
            sg.module.append(modul)
            module[modul.modul_id] = modul
        semester = {s.nummer: s for s in sg.semester}
        student = Student(
            data["matrikelnummer"],
            data["vorname"],
            data["nachname"],
            date.fromisoformat(data["studienbeginn"]),
            sg,
        )
        for b in data.get("belegungen", []):
            belegung = Belegung(
                module[b["modul_id"]],
                ModulStatus[b["status"]],
                semester.get(b["semester_nummer"]) if b.get("semester_nummer") else None,
            )
            pl = b.get("pruefungsleistung")
            if pl:
                belegung.pruefungsleistung = Pruefungsleistung(
                    Pruefungsart[pl["art"]],
                    pl["note"],
                    date.fromisoformat(pl["datum"]),
                    pl.get("seitenumfang"),
                    pl.get("dauer_minuten"),
                )
            student.belegungen.append(belegung)
        return student
