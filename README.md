# Studien-Dashboard

Eugen Loskan, Matrikelnummer: 9225210

Persönliches Dashboard zum Studienfortschritt (DLBDSOOFPP01_D - Objektorientierte und funktionale Programmierung mit Python).

Python 3.12, nur Standardbibliothek (tkinter, json). Kein pip.

## Start

    python main.py

Unter Windows auch: py main.py

Daten: daten.json im selben Ordner.

## Tests

    python run_all_tests.py

## Architektur

main.py startet Starter.
Starter erzeugt JsonRepository, DashboardService und DashboardApp.
Die GUI spricht nur den Service an. Der Student berechnet die Kennzahlen.