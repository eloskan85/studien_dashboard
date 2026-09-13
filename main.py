"""
Anwendungsebene.
main.py startet nur die Startklasse.
Aufruf: python main.py   oder unter Windows: py main.py
"""

from pathlib import Path
import sys

WURZEL = Path(__file__).resolve().parent
sys.path.insert(0, str(WURZEL))

from anwendung.starter import Starter


def main() -> None:
    """Uebergibt den Dateipfad an die Startklasse."""
    Starter(str(WURZEL / "daten.json")).starten()


if __name__ == "__main__":
    main()
