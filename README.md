# codex-playground

## StudyPilot – Lernsoftware für Technische Informatik

StudyPilot ist eine kleine, lokale Lernsoftware (CLI) mit einem einfachen AI‑Tutor,
Lernpfaden für Mathe und Python sowie Fortschrittsverwaltung. Die App ist bewusst
schlank gehalten, damit du sie leicht erweitern kannst.

### Features
- **Geführte Lernpfade**: Mathe‑Grundlagen, Analysis, Lineare Algebra, Diskrete Mathematik, Python‑Basics.
- **AI‑Tutor im Chat‑Stil**: Frage nach „Beispiel“, „Hilfe“ oder „Warum“ für kontextbasierte Antworten.
- **Fortschritt speichern**: abgeschlossene Lektionen und Verlauf werden lokal gespeichert.
- **Tagesstruktur**: 3‑Stunden‑Plan für konstantes Lernen.

---

## Installation & Start

Voraussetzung: Python 3.10+

```bash
python3 study_app.py
```

Beim ersten Start werden automatisch die Fortschrittsdateien im Ordner
`study_data/` angelegt.

---

## Datenstruktur

- `study_app.py` enthält die Lernsoftware (Menü, Tutor, Fortschritt).
- `study_data/lessons.json` enthält die Lektionen (leicht erweiterbar).
- `study_data/progress.json` wird automatisch erstellt und aktualisiert.

---

## Lektionen erweitern

Füge einfach neue Einträge in `study_data/lessons.json` hinzu. Beispiel:

```json
{
  "id": "NEU01",
  "track": "Python Basics",
  "title": "Listen verstehen",
  "summary": "Listen speichern mehrere Werte.",
  "key_points": ["Indexierung", "append()", "len()"],
  "exercise": "Erstelle eine Liste mit 5 Zahlen.",
  "example": "zahlen = [1, 2, 3, 4, 5]",
  "hint": "Nutze eckige Klammern."
}
```

---

## Zielgruppe & Lernmodus

Ideal für Lernende mit Grundkenntnissen in Algebra und ersten Python‑Schritten,
die sich auf ein Studium der Technischen Informatik vorbereiten und ca. 3 Stunden
pro Tag investieren wollen.
