import json
import os
import textwrap
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "study_data")
LESSONS_PATH = os.path.join(DATA_DIR, "lessons.json")
PROGRESS_PATH = os.path.join(DATA_DIR, "progress.json")


def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path, payload):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def wrap(text, width=78):
    return "\n".join(textwrap.wrap(text, width=width))


def header(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78 + "\n")


def pause():
    input("\nWeiter mit Enter...")


def list_tracks(lessons):
    return sorted({lesson["track"] for lesson in lessons})


def select_track(lessons):
    tracks = list_tracks(lessons)
    print("Verfügbare Lernpfade:")
    for idx, track in enumerate(tracks, start=1):
        print(f"  {idx}. {track}")
    choice = input("\nBitte Nummer wählen: ").strip()
    if not choice.isdigit():
        return tracks[0]
    index = max(1, min(len(tracks), int(choice)))
    return tracks[index - 1]


def show_lesson(lesson, progress):
    header(lesson["title"])
    print(wrap(lesson["summary"]))
    print("\nKernideen:")
    for item in lesson["key_points"]:
        print(f"  • {item}")
    print("\nÜbung:")
    print(wrap(lesson["exercise"]))
    progress["last_lesson"] = lesson["id"]
    progress["completed_lessons"].append(lesson["id"])
    progress["history"].append(
        {"lesson_id": lesson["id"], "timestamp": datetime.utcnow().isoformat()}
    )


def ai_tutor(prompt, lesson):
    prompt = prompt.lower()
    if any(word in prompt for word in ["warum", "wieso", "wies"]):
        return (
            "Gute Frage! Versuche den Begriff aus der Definition herzuleiten. "
            "Bei dieser Lektion heißt das: "
            f"{lesson['summary']}"
        )
    if "beispiel" in prompt:
        return (
            "Hier ist ein Beispiel-Ansatz: "
            f"{lesson['example']}"
        )
    if "hilfe" in prompt or "tipp" in prompt:
        return lesson["hint"]
    return (
        "Ich helfe gern weiter. Nutze Wörter wie 'Beispiel', 'Hilfe' oder "
        "'Warum', damit ich gezielt reagieren kann."
    )


def lesson_session(lessons, progress):
    track = select_track(lessons)
    track_lessons = [l for l in lessons if l["track"] == track]
    track_lessons.sort(key=lambda l: l["id"])

    for lesson in track_lessons:
        if lesson["id"] in progress["completed_lessons"]:
            continue
        show_lesson(lesson, progress)
        save_json(PROGRESS_PATH, progress)
        while True:
            answer = input("\nAI-Tutor (Frage stellen oder 'weiter'): ").strip()
            if answer.lower() in {"weiter", "next", ""}:
                break
            response = ai_tutor(answer, lesson)
            print("\nAI-Tutor:")
            print(wrap(response))
        pause()
        return

    header("Alle Lektionen abgeschlossen!")
    print("Du hast in diesem Lernpfad alle Lektionen abgeschlossen.")
    pause()


def review_progress(progress):
    header("Dein Fortschritt")
    completed = progress["completed_lessons"]
    if not completed:
        print("Noch keine Lektionen abgeschlossen.")
        pause()
        return
    print(f"Abgeschlossene Lektionen: {len(completed)}")
    last = progress.get("last_lesson")
    if last:
        print(f"Letzte Lektion: {last}")
    if progress["history"]:
        print("\nLetzte Aktivitäten:")
        for entry in progress["history"][-5:]:
            print(f"  • {entry['lesson_id']} @ {entry['timestamp']}")
    pause()


def daily_plan():
    header("Tagesstruktur (3 Stunden)")
    print("1. 60 Min Mathe Theorie + Beispiele")
    print("2. 60 Min Mathe/Python Anwendung")
    print("3. 60 Min Python + Mini-Projekt")
    pause()


def reset_progress():
    header("Fortschritt zurücksetzen")
    confirm = input("Wirklich alles löschen? (ja/nein): ").strip().lower()
    if confirm == "ja":
        save_json(PROGRESS_PATH, default_progress())
        print("Fortschritt wurde zurückgesetzt.")
    else:
        print("Abgebrochen.")
    pause()


def default_progress():
    return {"completed_lessons": [], "last_lesson": None, "history": []}


def main():
    lessons = load_json(LESSONS_PATH, default=[])
    progress = load_json(PROGRESS_PATH, default=default_progress())

    while True:
        header("StudyPilot — Technische Informatik Vorbereitung")
        print("1. Nächste Lektion starten")
        print("2. Fortschritt ansehen")
        print("3. Tagesstruktur anzeigen")
        print("4. Fortschritt zurücksetzen")
        print("5. Beenden")
        choice = input("\nAuswahl: ").strip()

        if choice == "1":
            lesson_session(lessons, progress)
        elif choice == "2":
            review_progress(progress)
        elif choice == "3":
            daily_plan()
        elif choice == "4":
            reset_progress()
            progress = load_json(PROGRESS_PATH, default=default_progress())
        elif choice == "5":
            print("Viel Erfolg beim Lernen!")
            break
        else:
            print("Bitte eine gültige Auswahl treffen.")


if __name__ == "__main__":
    main()
