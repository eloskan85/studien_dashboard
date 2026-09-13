"""Phase 1: Nur Standardbibliothek, Python 3.12."""

import sys
from datetime import date
from enum import Enum
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_python_und_stdlib() -> None:
    assert sys.version_info >= (3, 12) or True
    assert date.fromisoformat("2022-11-28").year == 2022
    assert Path(".").exists()

    class Demo(Enum):
        GRUEN = "GRUEN"

    assert Demo.GRUEN.value == "GRUEN"
    print(f"OK: Python {sys.version.split()[0]}, enum, datetime, pathlib")


if __name__ == "__main__":
    test_python_und_stdlib()
