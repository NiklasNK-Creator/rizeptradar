
# RecipeRadar

**RecipeRadar** ist ein schlanker Rezept-Generator für Windows, macOS und Linux.  
Gib einfach deine vorhandenen Zutaten ein und erhalte sofort Rezeptvorschläge, die passen.

## Features

- Zutaten-Eingabe (Komma getrennt)  
- Optionale Keyword- oder Tag-Suche  
- Sofortige Ergebnisliste mit Details  
- Einfache Erweiterung: Rezepte liegen in `data/recipes.json` (JSON-Liste)  

## Installation / Entwicklung

```bash
# 1. Repo klonen
git clone https://github.com/DEIN_NAME/RecipeRadar.git
cd RecipeRadar

# 2. Virtuelle Umgebung (optional)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Abhängigkeiten installieren
pip install -r requirements.txt

# 4. App starten
python main.py
```

## Rezepte hinzufügen

Öffne `data/recipes.json` und hänge einen neuen Eintrag an:

```json
{
    "id": 5,
    "name": "Pancakes",
    "ingredients": ["mehl", "milch", "ei", "backpulver", "salz"],
    "tags": ["frühstück", "süß"]
}
```

## .exe bauen (Windows)

```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --icon assets/icon.ico main.py
```

Die fertige EXE liegt danach unter `dist/main.exe`.

## Lizenz

MIT
