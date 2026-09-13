"""Phase 2: Belegung, Bestanden nur aus der Note."""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domain import Belegung, Modul, ModulStatus, Pruefungsart, Pruefungsleistung


def test_bestanden_nur_aus_der_note() -> None:
    modul = Modul("DLBDSOOFPP01", "OOP mit Python", 5)
    belegung = Belegung(modul, ModulStatus.BELEGT)
    assert belegung.ist_bestanden is False

    belegung.pruefungsleistung = Pruefungsleistung(
        Pruefungsart.PORTFOLIO,
        1.7,
        date.today(),
        dauer_minuten=90,
    )
    assert belegung.ist_bestanden is True
    assert belegung.pruefungsleistung.seitenumfang is None
    print("OK: Belegung + Note als Quelle")


if __name__ == "__main__":
    test_bestanden_nur_aus_der_note()
