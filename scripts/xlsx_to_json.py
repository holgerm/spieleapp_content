import pandas as pd
import json
import re
import sys
import os
from pathlib import Path

def parse_list_field(raw):
    if not isinstance(raw, str):
        return []
    return [re.sub(r'^"?slsspiele\.', '', s.strip().strip('"')) for s in raw.split(",") if s.strip()]

def convert_xlsx_to_json(xlsx_file, output_file, spiel_id):
    df = pd.read_excel(xlsx_file, header=None, names=["key", "value"])
    field_map = {
        "Spielname": "name",
        "Bildlink": "image",
        "Spieltypen": "categories",
        "Spieleranzahl": "numberOfPlayers",
        "Dauer": "durationOfGame",
        "Wetter": "weather",
        "Orte": "locations",
        "Kurzbeschreibung": "description",
        "Stichworte": "keywords",
        "Material": "material"
    }

    json_obj = {"id": spiel_id}

    for _, row in df.iterrows():
        excel_key = row["key"]
        value = row["value"]
        if pd.isna(excel_key) or pd.isna(value):
            continue
        key = field_map.get(excel_key)
        if not key:
            continue
        if key in ["categories", "numberOfPlayers", "durationOfGame", "weather", "locations", "keywords"]:
            json_obj[key] = parse_list_field(value)
        else:
            json_obj[key] = str(value).strip()

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(json_obj, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python bin/xlsx_to_json.py <input.xlsx> <output.json> <id>")
        sys.exit(1)
    convert_xlsx_to_json(sys.argv[1], sys.argv[2], sys.argv[3])