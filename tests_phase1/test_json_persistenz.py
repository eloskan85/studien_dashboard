"""Phase 1: JSON speichern und laden ohne Extra-Paket."""

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domain import Student, Studiengang


def test_json_rundreise() -> None:
    ziel = Path(__file__).with_name("_tmp_student.json")
    daten = {
        "matrikelnummer": "9225210",
        "vorname": "Eugen",
        "nachname": "Loskan",
        "studienbeginn": "2022-11-28",
        "studiengang": "Softwareentwicklung",
        "belegungen": [
            {
                "modul_id": "DLBDSOOFPP01",
                "name": "OOP mit Python",
                "ects": 5,
                "status": "BELEGT",
                "note": None,
            }
        ],
    }
    ziel.write_text(json.dumps(daten, indent=2), encoding="utf-8")
    geladen = json.loads(ziel.read_text(encoding="utf-8"))
    assert geladen["matrikelnummer"] == "9225210"
    assert geladen["belegungen"][0]["ects"] == 5

    sg = Studiengang(geladen["studiengang"])
    student = Student(
        geladen["matrikelnummer"],
        geladen["vorname"],
        geladen["nachname"],
        date.fromisoformat(geladen["studienbeginn"]),
        sg,
    )
    assert student.matrikelnummer == "9225210"
    print("OK: JSON laden und speichern ohne Extra-Paket")
    ziel.unlink(missing_ok=True)


if __name__ == "__main__":
    test_json_rundreise()
