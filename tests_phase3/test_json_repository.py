"""Phase 3: Persistenz. Enums, Datum und optionale Felder ueberleben Speichern/Laden."""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domain import Belegung, Modul, ModulStatus, Pruefungsart, Semester, SemesterStatus, Student, Studiengang
from persistenz import JsonRepository


def test_json_rundreise(tmp_dir: Path | None = None) -> None:
    ziel = Path(__file__).with_name("_tmp_repo.json")
    sg = Studiengang("Informatik", 180, 8)
    sem = Semester(1, "Semester 1", SemesterStatus.AKTUELL)
    modul = Modul("M1", "Mathematik I", 5)
    sg.semester.append(sem)
    sg.module.append(modul)
    student = Student("9225210", "Eugen", "Loskan", date(2024, 10, 1), sg)
    bel = Belegung(modul, ModulStatus.BELEGT, sem)
    bel.setze_note(1.7, Pruefungsart.KLAUSUR, date(2025, 2, 10))
    student.belegungen.append(bel)

    repo = JsonRepository(str(ziel))
    repo.speichern(student)
    geladen = repo.laden()

    assert geladen.matrikelnummer == "9225210"
    assert geladen.studienbeginn == date(2024, 10, 1)
    assert geladen.belegungen[0].pruefungsleistung.note == 1.7
    assert geladen.belegungen[0].pruefungsleistung.art is Pruefungsart.KLAUSUR
    assert geladen.belegungen[0].pruefungsleistung.seitenumfang is None
    assert geladen.ermittle_ziel_ampel().name == "GELB"
    print("OK: JSON mit Enum, Datum und None")
    ziel.unlink(missing_ok=True)


if __name__ == "__main__":
    test_json_rundreise()
