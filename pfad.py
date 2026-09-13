"""Macht den Projektordner für Imports auffindbar."""

from pathlib import Path
import sys

WURZEL = Path(__file__).resolve().parent
if str(WURZEL) not in sys.path:
    sys.path.insert(0, str(WURZEL))
