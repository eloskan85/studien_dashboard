"""Fachliches Domaenenmodell.

Pruefungsleistung haengt an der Belegung, Bestehen nur aus der Note,
Kennzahlen nur am Student, studienbeginn für den Zeitfortschritt.
"""

from __future__ import annotations

from datetime import date
from enum import Enum

# -----------------------------
# Feste Wertebereiche
# -----------------------------
class ModulStatus(Enum):
    """Fester Status einer Belegung."""

    GEPLANT = "GEPLANT"
    BELEGT = "BELEGT"
    BESTANDEN = "BESTANDEN"
    NICHT_BESTANDEN = "NICHT_BESTANDEN"


class Pruefungsart(Enum):
    """Art der Pruefung. Keine Unterklassen, weil kein eigenes Verhalten."""

    KLAUSUR = "KLAUSUR"
    PORTFOLIO = "PORTFOLIO"
    PROJEKTBERICHT = "PROJEKTBERICHT"
    FALLSTUDIE = "FALLSTUDIE"


class SemesterStatus(Enum):
    """Status eines Semesters im Studienverlauf."""

    GEPLANT = "GEPLANT"
    AKTUELL = "AKTUELL"
    ABGESCHLOSSEN = "ABGESCHLOSSEN"


class AmpelStatus(Enum):
    """Zielampel zum Gesamtschnitt unter 2,0."""

    GRUEN = "GRUEN"
    GELB = "GELB"
    ROT = "ROT"

# -----------------------------
# Domäne
# -----------------------------
class Studiengang:
    """Semester und Module. Keine Berechnungen."""

    def __init__(self, name: str, gesamtects: int = 180, max_semester: int = 8) -> None:
        self.name = name
        self.gesamtects = gesamtects
        self.max_semester = max_semester
        self.semester: list[Semester] = []
        self.module: list[Modul] = []


class Semester:
    """Zeitliche Einheit. Status als Enumeration."""

    def __init__(self, nummer: int, bezeichnung: str, status: SemesterStatus) -> None:
        self.nummer = nummer
        self.bezeichnung = bezeichnung
        self.status = status


class Modul:
    """Katalogmodul des Studiengangs. Ohne Note und ohne Status."""

    def __init__(self, modul_id: str, name: str, ects: int) -> None:
        self.modul_id = modul_id
        self.name = name
        self.ects = ects


class Pruefungsleistung:
    """Individuelles Pruefungsergebnis einer Belegung.

    seitenumfang und dauer_minuten sind optional, weil sie nicht
    für jede Pruefungsart gelten.
    """

    def __init__(
        self,
        art: Pruefungsart,
        note: float,
        datum: date,
        seitenumfang: int | None = None,
        dauer_minuten: int | None = None,
    ) -> None:
        self.art = art
        self.note = note
        self.datum = datum
        self.seitenumfang = seitenumfang
        self.dauer_minuten = dauer_minuten


class Belegung:
    """Verbindung von Student und Modul. Hier liegen Status, Semester und Note."""

    def __init__(
        self,
        modul: Modul,
        status: ModulStatus = ModulStatus.GEPLANT,
        semester: Semester | None = None,
    ) -> None:
        self.modul = modul
        self.status = status
        self.semester = semester
        self.pruefungsleistung: Pruefungsleistung | None = None

    @property
    def ist_bestanden(self) -> bool:
        """True, wenn eine Note vorliegt und diese 4,0 oder besser ist."""
        if self.pruefungsleistung is None:
            return False
        return self.pruefungsleistung.note <= 4.0

    def setze_note(self, note: float, art: Pruefungsart, datum: date) -> None:
        """Legt die Pruefungsleistung an und leitet den Status aus der Note ab."""
        self.pruefungsleistung = Pruefungsleistung(art, note, datum)
        self.status = ModulStatus.BESTANDEN if self.ist_bestanden else ModulStatus.NICHT_BESTANDEN


class Student:
    """Studierende Person. Alle Kennzahlen und die Ampel liegen hier."""

    def __init__(
        self,
        matrikelnummer: str,
        vorname: str,
        nachname: str,
        studienbeginn: date,
        studiengang: Studiengang,
    ) -> None:
        self._matrikelnummer = matrikelnummer
        self.vorname = vorname
        self.nachname = nachname
        self.studienbeginn = studienbeginn
        self.studiengang = studiengang
        self.belegungen: list[Belegung] = []

    @property
    def matrikelnummer(self) -> str:
        """Lesen der gekapselten Matrikelnummer."""
        return self._matrikelnummer

    def berechne_notendurchschnitt(self) -> float:
        """ECTS-gewichteter Schnitt aller vorhandenen Noten. Ohne Note 0,0."""
        gewicht = 0.0
        ects_summe = 0
        for belegung in self.belegungen:
            pl = belegung.pruefungsleistung
            if pl is None:
                continue
            gewicht += pl.note * belegung.modul.ects
            ects_summe += belegung.modul.ects
        if ects_summe == 0:
            return 0.0
        return gewicht / ects_summe

    def berechne_ects_fortschritt(self) -> float:
        """Bestandene ECTS im Verhaeltnis zu 180, in Prozent."""
        erreicht = sum(b.modul.ects for b in self.belegungen if b.ist_bestanden)
        return (erreicht / self.studiengang.gesamtects) * 100

    def berechne_zeitfortschritt(self, heute: date | None = None) -> float:
        """Fachsemester aus studienbeginn im Verhaeltnis zu acht Semestern."""
        heute = heute or date.today()
        monate = (heute.year - self.studienbeginn.year) * 12 + (heute.month - self.studienbeginn.month)
        fachsemester = max(1, monate // 6 + 1)
        return min(100.0, (fachsemester / self.studiengang.max_semester) * 100)

    def ermittle_ziel_ampel(self) -> AmpelStatus:
        """gruen < 1,7; gelb >= 1,7 und < 2,0; rot >= 2,0. Ohne Note gelb."""
        schnitt = self.berechne_notendurchschnitt()
        if schnitt == 0.0:
            return AmpelStatus.GELB
        if schnitt < 1.7:
            return AmpelStatus.GRUEN
        if schnitt < 2.0:
            return AmpelStatus.GELB
        return AmpelStatus.ROT
