import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox,
    QPushButton, QLabel, QCheckBox, QListWidget, QListWidgetItem,
    QGroupBox, QMessageBox, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt

# Eingebettete Daten
DATA = {
    "ingredients": [
        "Spaghetti", "Eier", "Guanciale", "Pecorino Romano", "Schwarzer Pfeffer", "Salz",
        "Olivenöl", "Knoblauch", "Chili", "Petersilie", "Tomaten", "Mozzarella", "Basilikum",
        "Balsamico", "Avocado", "Vollkornbrot", "Zitrone", "Pfeffer", "Hähnchenbrust",
        "Zwiebeln", "Ingwer", "Currypaste", "Kokosmilch", "Reis"
    ],
    "tags": [
        "italienisch", "klassisch", "vegetarisch", "schnell", "salat", "einfach",
        "frühstück", "gesund", "asiatisch", "mit Fleisch", "herzhaft"
    ],
    "recipes": [
        {
            "id": 1,
            "name": "Spaghetti Carbonara",
            "ingredients": ["Spaghetti", "Eier", "Guanciale", "Pecorino Romano", "Schwarzer Pfeffer", "Salz"],
            "tags": ["italienisch", "klassisch"],
            "instructions": [
                "Spaghetti in reichlich Salzwasser al dente kochen.",
                "Guanciale in Würfel schneiden und in einer Pfanne knusprig auslassen.",
                "Eier mit geriebenem Pecorino und Pfeffer verquirlen.",
                "Spaghetti abgießen, etwas Kochwasser auffangen.",
                "Guanciale und Spaghetti vermengen, Pfanne vom Herd nehmen.",
                "Eimischung unterrühren, falls nötig etwas Kochwasser zugeben.",
                "Sofort servieren, mit extra Pecorino und Pfeffer bestreuen."
            ]
        },
        {
            "id": 2,
            "name": "Spaghetti Aglio e Olio",
            "ingredients": ["Spaghetti", "Olivenöl", "Knoblauch", "Chili", "Petersilie", "Salz"],
            "tags": ["italienisch", "vegetarisch", "schnell"],
            "instructions": [
                "Spaghetti in Salzwasser kochen.",
                "Olivenöl in einer Pfanne erhitzen, Knoblauch und Chili anbraten.",
                "Spaghetti abgießen und in die Pfanne geben.",
                "Gut durchmischen, mit Petersilie bestreuen und servieren."
            ]
        },
        {
            "id": 3,
            "name": "Tomaten-Mozzarella-Salat",
            "ingredients": ["Tomaten", "Mozzarella", "Basilikum", "Olivenöl", "Balsamico", "Salz", "Pfeffer"],
            "tags": ["salat", "vegetarisch", "einfach"],
            "instructions": [
                "Tomaten und Mozzarella in Scheiben schneiden.",
                "Abwechselnd auf einem Teller anrichten.",
                "Mit Basilikum belegen.",
                "Mit Olivenöl, Balsamico, Salz und Pfeffer abschmecken."
            ]
        }
    ]
}


class RecipeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rezept-Finder")
        self.resize(1000, 700)
        self.data = DATA
        self.favourites = set()

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        # Titel und Suche
        title = QLabel("🍲 Rezept-Finder")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title)

        self.search_criteria = QComboBox()
        self.search_criteria.addItems(["Nach Zutaten suchen", "Nach Tags suchen"])
        main_layout.addWidget(self.search_criteria)

        # Oberes Layout: Zutaten – Rezepte – Tags
        top_layout = QHBoxLayout()

        # Zutaten links
        self.ingredient_checkboxes = []
        ingr_widget = QWidget()
        ingr_layout = QVBoxLayout(ingr_widget)
        for ingr in self.data["ingredients"]:
            cb = QCheckBox(ingr)
            self.ingredient_checkboxes.append(cb)
            ingr_layout.addWidget(cb)

        ingr_scroll = QScrollArea()
        ingr_scroll.setWidgetResizable(True)
        ingr_scroll.setWidget(ingr_widget)
        ingr_scroll.setFixedWidth(220)
        top_layout.addWidget(ingr_scroll)

        # Rezeptliste in der Mitte
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.show_recipe_details)
        self.list_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        top_layout.addWidget(self.list_widget, stretch=2)

        # Tags rechts
        self.tag_combo = QComboBox()
        self.tag_combo.addItem("Alle Tags")
        self.tag_combo.addItems(self.data["tags"])
        self.tag_combo.setMinimumWidth(180)

        tag_layout = QVBoxLayout()
        tag_layout.addWidget(QLabel("Tags auswählen:"))
        tag_layout.addWidget(self.tag_combo)
        tag_layout.addStretch()

        tag_container = QWidget()
        tag_container.setLayout(tag_layout)
        tag_scroll = QScrollArea()
        tag_scroll.setWidgetResizable(True)
        tag_scroll.setWidget(tag_container)
        tag_scroll.setFixedWidth(200)
        top_layout.addWidget(tag_scroll)

        main_layout.addLayout(top_layout)

        # Buttons
        btn_row = QHBoxLayout()
        self.btn_search = QPushButton("Suchen")
        self.btn_all = QPushButton("Alle Rezepte")
        self.btn_fav = QPushButton("Favoriten")
        btn_row.addWidget(self.btn_search)
        btn_row.addWidget(self.btn_all)
        btn_row.addWidget(self.btn_fav)
        main_layout.addLayout(btn_row)

        # Detailansicht
        self.detail_label = QLabel()
        self.detail_label.setWordWrap(True)
        self.detail_label.setTextFormat(Qt.TextFormat.RichText)
        self.detail_label.hide()
        main_layout.addWidget(self.detail_label)

        self.btn_back = QPushButton("Zurück")
        self.btn_toggle_fav = QPushButton()
        self.btn_back.clicked.connect(self.hide_details)
        self.btn_toggle_fav.clicked.connect(self.toggle_favourite)
        self.btn_back.hide()
        self.btn_toggle_fav.hide()

        btn_detail_row = QHBoxLayout()
        btn_detail_row.addWidget(self.btn_toggle_fav)
        btn_detail_row.addStretch()
        btn_detail_row.addWidget(self.btn_back)
        main_layout.addLayout(btn_detail_row)

        # Events
        self.btn_search.clicked.connect(self.search)
        self.btn_all.clicked.connect(self.show_all_recipes)
        self.btn_fav.clicked.connect(self.show_favourites)

        self.current_recipes = []
        self.current_recipe = None
        self.show_all_recipes()

    def search(self):
        if self.search_criteria.currentText() == "Nach Zutaten suchen":
            selected = [cb.text() for cb in self.ingredient_checkboxes if cb.isChecked()]
            results = [r for r in self.data["recipes"] if set(r["ingredients"]).intersection(selected)] if selected else []
        else:
            tag = self.tag_combo.currentText()
            results = self.data["recipes"] if tag == "Alle Tags" else [r for r in self.data["recipes"] if tag in r["tags"]]

        if not results:
            QMessageBox.information(self, "Keine Treffer", "Keine Rezepte gefunden.")
        self.display_recipes(results)

    def show_all_recipes(self):
        self.display_recipes(self.data["recipes"])

    def show_favourites(self):
        favs = [r for r in self.data["recipes"] if r["id"] in self.favourites]
        if not favs:
            QMessageBox.information(self, "Keine Favoriten", "Noch keine Favoriten markiert.")
        self.display_recipes(favs)

    def display_recipes(self, recipes):
        self.list_widget.clear()
        for r in recipes:
            star = "★ " if r["id"] in self.favourites else ""
            item = QListWidgetItem(f"{star}{r['name']}")
            item.setData(Qt.ItemDataRole.UserRole, r)
            self.list_widget.addItem(item)
        self.current_recipes = recipes

    def show_recipe_details(self, item: QListWidgetItem):
        r = item.data(Qt.ItemDataRole.UserRole)
        self.current_recipe = r
        self.detail_label.setText(self.format_recipe(r))
        self.detail_label.show()
        self.btn_back.show()
        self.btn_toggle_fav.setText("Aus Favoriten entfernen" if r["id"] in self.favourites else "Als Favorit markieren")
        self.btn_toggle_fav.show()
        self.list_widget.hide()

    def hide_details(self):
        self.detail_label.hide()
        self.btn_back.hide()
        self.btn_toggle_fav.hide()
        self.list_widget.show()

    def toggle_favourite(self):
        if not self.current_recipe:
            return
        rid = self.current_recipe["id"]
        if rid in self.favourites:
            self.favourites.remove(rid)
        else:
            self.favourites.add(rid)
        self.btn_toggle_fav.setText("Aus Favoriten entfernen" if rid in self.favourites else "Als Favorit markieren")
        self.display_recipes(self.current_recipes)

    def format_recipe(self, r):
        steps = "<br>".join(f"{i+1}. {s}" for i, s in enumerate(r["instructions"]))
        return (
            f"<h3>{r['name']}</h3>"
            f"<b>Zutaten:</b> {', '.join(r['ingredients'])}<br>"
            f"<b>Tags:</b> {', '.join(r['tags'])}<br><br>"
            f"<b>Anleitung:</b><br>{steps}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RecipeApp()
    window.show()
    sys.exit(app.exec())
