"""Phase 2: Klasse, Objekt und Kapselung."""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domain import Student, Studiengang


def test_student_objekt_und_property() -> None:
    studiengang = Studiengang("Softwareentwicklung")
    student = Student(
        matrikelnummer="9225210",
        vorname="Eugen",
        nachname="Loskan",
        studienbeginn=date(2022, 11, 28),
        studiengang=studiengang,
    )
    assert student.matrikelnummer == "9225210"
    assert student.studienbeginn == date(2022, 11, 28)
    assert student.vorname == "Eugen"
    print("OK: Student-Objekt mit studienbeginn über die Instanz lesbar")


if __name__ == "__main__":
    test_student_objekt_und_property()
