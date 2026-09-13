"""Phase 2: Ampelgrenzen und Notendurchschnitt."""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domain import (
    AmpelStatus,
    Belegung,
    Modul,
    ModulStatus,
    Pruefungsart,
    Student,
    Studiengang,
)


def _student_mit_noten(noten: list[float]) -> Student:
    sg = Studiengang("Softwareentwicklung", gesamtects=180, max_semester=8)
    student = Student("9225210", "Eugen", "Loskan", date(2024, 10, 1), sg)
    for i, note in enumerate(noten, start=1):
        modul = Modul(f"M{i}", f"Modul {i}", 5)
        belegung = Belegung(modul, ModulStatus.BELEGT)
        belegung.setze_note(note, Pruefungsart.KLAUSUR, date.today())
        student.belegungen.append(belegung)
    return student


def test_ampelgrenzen() -> None:
    student = _student_mit_noten([1.3, 2.0])
    schnitt = student.berechne_notendurchschnitt()
    assert round(schnitt, 2) == 1.65
    assert student.ermittle_ziel_ampel() is AmpelStatus.GRUEN
    assert _student_mit_noten([1.8]).ermittle_ziel_ampel() is AmpelStatus.GELB
    assert _student_mit_noten([2.0]).ermittle_ziel_ampel() is AmpelStatus.ROT
    print("OK: 1,65 GRUEN, 1,8 GELB, 2,0 ROT")


if __name__ == "__main__":
    test_ampelgrenzen()
