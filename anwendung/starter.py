"""Startklasse. Verbindet Datei, Service und Oberflaeche."""

from __future__ import annotations

from anwendung.dashboard_service import DashboardService
from gui.dashboard_app import DashboardApp
from persistenz.json_repository import JsonRepository


class Starter:
    """
    Verantwortlich: Programmstart.
    Erzeugt Repository, Service und GUI. Rechnet nicht.
    """

    def __init__(self, dateipfad: str) -> None:
        self.repository = JsonRepository(dateipfad)
        self.service = DashboardService(self.repository)

    def starten(self) -> None:
        """Laedt die Daten und oeffnet das Fenster."""
        self.service.lade_daten()
        DashboardApp(self.service).start()
