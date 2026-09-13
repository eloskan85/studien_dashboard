"""Phase 3: Service reicht durch; Zeitfortschritt nutzt studienbeginn."""

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from anwendung.dashboard_service import DashboardService
from persistenz.json_repository import JsonRepository


def test_zeit_und_service() -> None:
    quelle = Path(__file__).resolve().parents[1] / "daten.json"
    service = DashboardService(JsonRepository(str(quelle)))
    student = service.lade_daten()

    assert student.studienbeginn == date(2022, 11, 28)
    zeit = student.berechne_zeitfortschritt(heute=date(2023, 11, 28))
    assert zeit == 37.5  # 12 Monate = Fachsemester 3 von 8

    assert service.notendurchschnitt() == student.berechne_notendurchschnitt()
    assert service.ampel() is student.ermittle_ziel_ampel()
    assert abs(service.ects_fortschritt() - student.berechne_ects_fortschritt()) < 0.01
    print("OK: Zeit aus studienbeginn, Service spiegelt den Student")


if __name__ == "__main__":
    test_zeit_und_service()
