"""Phase 2: Enumerationen statt Vererbung."""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domain import Pruefungsart, Pruefungsleistung, SemesterStatus


def test_pruefungsart_ist_enum_keine_unterklasse() -> None:
    klausur = Pruefungsleistung(
        art=Pruefungsart.KLAUSUR,
        note=1.7,
        datum=date.today(),
        dauer_minuten=90,
    )
    portfolio = Pruefungsleistung(
        art=Pruefungsart.PORTFOLIO,
        note=1.3,
        datum=date.today(),
        seitenumfang=5,
    )
    assert klausur.art is Pruefungsart.KLAUSUR
    assert portfolio.art is Pruefungsart.PORTFOLIO
    assert type(klausur) is type(portfolio)
    assert SemesterStatus.AKTUELL in SemesterStatus
    print("OK: ENUM statt Vererbung, optionale Merkmale je Art")


if __name__ == "__main__":
    test_pruefungsart_ist_enum_keine_unterklasse()
