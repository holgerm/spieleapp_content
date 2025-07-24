import os
import json
import sys

def generate_index(base_dir):
    items_dir = os.path.join(base_dir, "items")
    index = []

    for entry in os.listdir(items_dir):
        entry_path = os.path.join(items_dir, entry)
        content_path = os.path.join(entry_path, "content.json")

        if os.path.isdir(entry_path) and entry.isdigit() and os.path.isfile(content_path):
            try:
                with open(content_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    index.append({
                        "id": data.get("id", entry),
                        "name": data.get("name", "Unbenannt")
                    })
            except Exception as e:
                print(f"⚠️ Fehler beim Verarbeiten von {content_path}: {e}")

    # Nach ID sortieren (numerisch)
    index.sort(key=lambda x: int(x["id"]))

    # index.json schreiben
    index_path = os.path.join(items_dir, "index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=4, ensure_ascii=False)

    print(f"✅ index.json erfolgreich geschrieben mit {len(index)} Einträgen.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Nutzung: python generate_index.py <Basisverzeichnis>")
        sys.exit(1)

    base_dir = sys.argv[1]
    generate_index(base_dir)