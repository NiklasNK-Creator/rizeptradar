import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QScrollArea, QGroupBox, QCheckBox
from PyQt6.QtGui import QIcon

# Beispiel-Daten für Rezepte
recipes = [
    {
        "name": "Spaghetti Carbonara",
        "ingredients": ["Spaghetti", "Eier", "Bacon", "Käse", "Pfeffer", "Salz"],
        "instructions": [
            "Spaghetti kochen.",
            "Bacon anbraten.",
            "Eier mit Käse vermengen.",
            "Spaghetti mit Bacon und Eiern mischen.",
            "Mit Pfeffer und Salz abschmecken."
        ],
        "tags": ["Pastagericht", "Schnell", "Klassiker"]
    },
    # Weitere Rezepte hinzufügen...
]

class RecipeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recipe Radar")
        self.setWindowIcon(QIcon("assets/icon.png"))  # Dein Icon
        self.setGeometry(100, 100, 600, 400)

        # Layout
        self.layout = QVBoxLayout()

        # Eingabefeld für die Rezeptsuche
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Suche nach einem Rezept...")
        self.layout.addWidget(self.search_input)

        # Dropdown für Tags (Kategorien)
        self.tag_dropdown = QComboBox(self)
        self.tag_dropdown.addItem("Alle Kategorien")
        self.tag_dropdown.addItem("Pastagerichte")
        self.tag_dropdown.addItem("Vegetarisch")
        self.layout.addWidget(self.tag_dropdown)

        # Button zum Suchen
        self.search_button = QPushButton("Suche", self)
        self.search_button.clicked.connect(self.search_recipe)
        self.layout.addWidget(self.search_button)

        # Scrollbereich für die Rezepte
        self.recipe_area = QScrollArea(self)
        self.recipe_area.setWidgetResizable(True)
        self.layout.addWidget(self.recipe_area)

        # Hauptcontainer für Rezepte
        self.recipe_container = QWidget()
        self.recipe_area.setWidget(self.recipe_container)

        self.setLayout(self.layout)

    def search_recipe(self):
        search_term = self.search_input.text().lower()
        selected_tag = self.tag_dropdown.currentText()

        # Filtere Rezepte basierend auf der Suche und Tag
        filtered_recipes = []
        for recipe in recipes:
            if (search_term in recipe["name"].lower() or any(search_term in ingredient.lower() for ingredient in recipe["ingredients"])) and \
               (selected_tag == "Alle Kategorien" or selected_tag in recipe["tags"]):
                filtered_recipes.append(recipe)

        self.display_recipes(filtered_recipes)

    def display_recipes(self, recipes_to_display):
        # Lösche alle aktuellen Rezepte im Layout
        for i in reversed(range(self.recipe_container.layout().count())):
            widget = self.recipe_container.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Zeige die Rezepte an
        for recipe in recipes_to_display:
            recipe_box = QGroupBox(recipe["name"], self)
            recipe_layout = QVBoxLayout()

            # Zutaten
            ingredients_label = QLabel("Zutaten:")
            ingredients_text = "\n".join(f"- {ingredient}" for ingredient in recipe["ingredients"])
            ingredients_label.setText(ingredients_label.text() + "\n" + ingredients_text)

            # Zubereitung
            instructions_label = QLabel("Zubereitung:")
            instructions_text = "\n".join(f"{i+1}. {step}" for i, step in enumerate(recipe["instructions"]))
            instructions_label.setText(instructions_label.text() + "\n" + instructions_text)

            recipe_layout.addWidget(ingredients_label)
            recipe_layout.addWidget(instructions_label)

            # Tags
            tags_label = QLabel("Tags:")
            tags_text = ", ".join(recipe["tags"])
            tags_label.setText(tags_label.text() + " " + tags_text)
            recipe_layout.addWidget(tags_label)

            recipe_box.setLayout(recipe_layout)
            self.recipe_container.layout().addWidget(recipe_box)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RecipeApp()
    window.show()
    sys.exit(app.exec())
