"""Alle Tests nacheinander starten. In PyCharm diese Datei ausfuehren."""

import runpy
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent
sys.path.insert(0, str(WURZEL))

dateien = [
    WURZEL / "tests_phase1" / "test_standardbibliothek.py",
    WURZEL / "tests_phase1" / "test_json_persistenz.py",
    WURZEL / "tests_phase2" / "test_kapselung.py",
    WURZEL / "tests_phase2" / "test_enum_keine_vererbung.py",
    WURZEL / "tests_phase2" / "test_belegung_pruefung.py",
    WURZEL / "tests_phase2" / "test_ampelgrenzen.py",
    WURZEL / "tests_phase3" / "test_json_repository.py",
    WURZEL / "tests_phase3" / "test_service_und_zeit.py",
    WURZEL / "tests_phase1" / "test_tkinter_verfuegbar.py",
]

print("Projektwurzel:", WURZEL)
for datei in dateien:
    print("-" * 60)
    print("Starte", datei.name)
    try:
        runpy.run_path(str(datei), run_name="__main__")
    except ModuleNotFoundError as exc:
        print("UEBERSPRUNGEN:", exc)
print("-" * 60)
print("Fertig.")
