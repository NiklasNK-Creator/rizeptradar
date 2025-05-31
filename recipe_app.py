import sys, json, random
from pathlib import Path
from typing import Dict, Any

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QCheckBox, QListWidget, QListWidgetItem, QGroupBox,
    QMessageBox, QScrollArea, QSizePolicy, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextDocument
from PyQt6.QtPrintSupport import QPrinter


# ── Eingebettete Daten  (30 Rezepte) ─────────────────────────────────────────
DATA = {
    "ingredients": [
        # Basis
        "Spaghetti", "Eier", "Guanciale", "Pecorino Romano", "Schwarzer Pfeffer", "Salz",
        "Olivenöl", "Knoblauch", "Chili", "Petersilie", "Tomaten", "Mozzarella", "Basilikum",
        "Balsamico", "Avocado", "Vollkornbrot", "Zitrone", "Pfeffer", "Hähnchenbrust",
        "Zwiebeln", "Ingwer", "Currypaste", "Kokosmilch", "Reis", "Butter", "Mehl", "Milch",
        "Parmesan", "Rinderhack", "Kidneybohnen", "Mais", "Tortilla Wraps", "Gouda",
        "Paprika", "Kartoffeln", "Brokkoli", "Lachsfilet", "Sahne", "Dill", "Kichererbsen",
        "Rote Linsen", "Kreuzkümmel", "Koriander", "Joghurt", "Honig", "Sojasauce",
        "Sesamöl", "Frühlingszwiebeln", "Sesam", "Panko", "Paniermehl", "Nudeln",
        "Schmand", "Thunfisch", "Erbsen", "Feta", "Spinat", "Ricotta", "Blätterteig",
        "Hackfleisch", "Tomatenmark", "Oregano", "Rosmarin", "Kartoffelgnocchi", "Salsiccia",
        "Schwarze Oliven", "Kapern", "Lemon Curd", "Mascarpone", "Zucker", "Gelatine",
        "Vanilleschote", "Hefeteig", "Zimt", "Brauner Zucker"
    ],
    "tags": [
        "italienisch", "klassisch", "vegetarisch", "schnell", "salat", "einfach",
        "frühstück", "gesund", "asiatisch", "mit Fleisch", "herzhaft", "sweet",
        "vegan", "fisch", "backen", "auflauf"
    ],
    "recipes": [
        {
            "id": 1,
            "name": "Spaghetti Carbonara",
            "ingredients": ["Spaghetti","Eier","Guanciale","Pecorino Romano","Schwarzer Pfeffer","Salz"],
            "tags": ["italienisch","klassisch"],
            "instructions": [
                "Spaghetti in reichlich Salzwasser al dente kochen.",
                "Guanciale würfeln und in einer Pfanne knusprig auslassen.",
                "Eier mit fein geriebenem Pecorino und Pfeffer verquirlen.",
                "Spaghetti abgießen, etwas Kochwasser auffangen.",
                "Spaghetti und Guanciale mischen, Pfanne vom Herd.",
                "Eimischung rasch unterrühren, bei Bedarf Kochwasser zugeben.",
                "Sofort servieren und mit extra Pecorino bestreuen."
            ]
        },
        {
            "id": 2,
            "name": "Spaghetti Aglio e Olio",
            "ingredients": ["Spaghetti","Olivenöl","Knoblauch","Chili","Petersilie","Salz"],
            "tags": ["italienisch","vegetarisch","schnell"],
            "instructions": [
                "Spaghetti in Salzwasser garen.",
                "Öl in großer Pfanne erhitzen, Knoblauchscheiben & Chili anrösten.",
                "Spaghetti abgießen, ½ Kelle Kochwasser aufheben.",
                "Pasta ins Öl geben, schwenken, Petersilie zufügen.",
                "Mit Kochwasser binden, abschmecken, sofort servieren."
            ]
        },
        {
            "id": 3,
            "name": "Tomaten-Mozzarella-Salat",
            "ingredients": ["Tomaten","Mozzarella","Basilikum","Olivenöl","Balsamico","Salz","Pfeffer"],
            "tags": ["salat","vegetarisch","einfach"],
            "instructions": [
                "Tomaten & Mozzarella in Scheiben schneiden.",
                "Abwechselnd auf Teller fächern.",
                "Mit Basilikumblättern belegen.",
                "Öl & Balsamico darüberträufeln, salzen & pfeffern."
            ]
        },
        {
            "id": 4,
            "name": "Avocado-Toast",
            "ingredients": ["Avocado","Vollkornbrot","Olivenöl","Chili","Zitrone","Salz","Pfeffer"],
            "tags": ["frühstück","gesund","einfach"],
            "instructions": [
                "Brot toasten.",
                "Avocado zerdrücken, mit Zitronensaft, Salz, Pfeffer mischen.",
                "Creme aufs Brot, Chili-Flocken & Olivenöl darüber."
            ]
        },
        {
            "id": 5,
            "name": "Chicken Curry",
            "ingredients": ["Hähnchenbrust","Zwiebeln","Knoblauch","Ingwer","Currypaste","Kokosmilch","Reis"],
            "tags": ["asiatisch","mit Fleisch","herzhaft"],
            "instructions": [
                "Hähnchen würfeln, Zwiebeln, Knoblauch, Ingwer hacken.",
                "Öl erhitzen, Fleisch anbraten, Zwiebelmischung zugeben.",
                "Currypaste einrühren, kurz rösten.",
                "Mit Kokosmilch aufgießen, 15 min köcheln lassen.",
                "Mit Reis servieren."
            ]
        },
        {
            "id": 6,
            "name": "Käse-Brokkoli-Auflauf",
            "ingredients": ["Brokkoli","Butter","Mehl","Milch","Parmesan","Gouda","Salz","Pfeffer"],
            "tags": ["auflauf","vegetarisch","klassisch"],
            "instructions": [
                "Brokkoli in Röschen teilen, blanchieren.",
                "Butter schmelzen, Mehl anschwitzen, Milch einrühren – Béchamel kochen.",
                "Parmesan einrühren, würzen.",
                "Brokkoli in Auflaufform, Sauce darüber, Gouda bestreuen.",
                "20 Minuten bei 200 °C backen."
            ]
        },
        {
            "id": 7,
            "name": "Lachs in Dill-Sahne",
            "ingredients": ["Lachsfilet","Sahne","Dill","Zitrone","Salz","Pfeffer"],
            "tags": ["fisch","schnell","gesund"],
            "instructions": [
                "Lachs salzen, pfeffern, in Pfanne anbraten.",
                "Sahne und Zitronensaft angießen, Dill zugeben.",
                "5-7 min ziehen lassen, Sauce abschmecken.",
                "Mit Reis oder Kartoffeln servieren."
            ]
        },
        {
            "id": 8,
            "name": "Chili con Carne",
            "ingredients": ["Rinderhack","Zwiebeln","Knoblauch","Kidneybohnen","Mais","Tomaten","Chili","Tomatenmark","Paprika","Oregano","Salz","Pfeffer"],
            "tags": ["mit Fleisch","herzhaft"],
            "instructions": [
                "Hack krümelig anbraten.",
                "Zwiebeln, Knoblauch, Paprika zugeben, anschwitzen.",
                "Tomatenmark einrühren, kurz rösten.",
                "Tomaten, Bohnen, Mais, Chili, Oregano zugeben.",
                "30 Minuten köcheln, abschmecken."
            ]
        },
        {
            "id": 9,
            "name": "Vegetarische Lasagne",
            "ingredients": ["Lasagneplatten","Zucchini","Aubergine","Tomaten","Mozzarella","Ricotta","Basilikum","Olivenöl","Knoblauch","Oregano","Salz","Pfeffer"],
            "tags": ["auflauf","vegetarisch"],
            "instructions": [
                "Gemüse würfeln, in Öl anbraten, würzen.",
                "Ricotta mit gehacktem Basilikum verrühren.",
                "Auflaufform schichten: Sauce, Platten, Ricotta, Gemüse, wiederholen.",
                "Mit Mozzarella abschließen, 35 Minuten 190 °C backen."
            ]
        },
        {
            "id": 10,
            "name": "Ofenkartoffeln mit Feta",
            "ingredients": ["Kartoffeln","Olivenöl","Rosmarin","Feta","Pfeffer","Salz"],
            "tags": ["vegetarisch","einfach"],
            "instructions": [
                "Kartoffeln halbieren, mit Öl, Salz, Rosmarin mischen.",
                "Auf Blech 30 Minuten 200 °C backen.",
                "Mit zerbröseltem Feta bestreuen."
            ]
        },
        {
            "id": 11,
            "name": "Linsen-Dal",
            "ingredients": ["Rote Linsen","Zwiebeln","Knoblauch","Ingwer","Kreuzkümmel","Koriander","Currypaste","Kokosmilch","Salz"],
            "tags": ["vegan","asiatisch","gesund"],
            "instructions": [
                "Gewürze trocken rösten, dann Öl zugeben.",
                "Zwiebeln, Knoblauch, Ingwer anschwitzen.",
                "Linsen einrühren, Currypaste zugeben.",
                "Kokosmilch & Wasser auffüllen, 20 min köcheln.",
                "Mit Salz abschmecken."
            ]
        },
        {
            "id": 12,
            "name": "Cremige One-Pot-Pasta",
            "ingredients": ["Nudeln","Sahne","Parmesan","Knoblauch","Spinat","Pfeffer","Salz"],
            "tags": ["schnell","vegetarisch"],
            "instructions": [
                "Nudeln mit Wasser & Sahne aufkochen.",
                "Knoblauch und Spinat hinzufügen.",
                "Reduzieren, bis Nudeln gar & Sauce cremig.",
                "Parmesan unterrühren, würzen."
            ]
        },
        {
            "id": 13,
            "name": "Thunfisch-Erbsen-Nudelauflauf",
            "ingredients": ["Nudeln","Thunfisch","Erbsen","Schmand","Gouda","Pfeffer","Salz"],
            "tags": ["auflauf","schnell"],
            "instructions": [
                "Nudeln knapp gar kochen.",
                "Schmand mit Thunfisch + Erbsen mischen, würzen.",
                "Alles in Form, Gouda darüber, 15 min bei 200 °C überbacken."
            ]
        },
        {
            "id": 14,
            "name": "Falafel-Wrap",
            "ingredients": ["Kichererbsen","Knoblauch","Petersilie","Kreuzkümmel","Panko","Tortilla Wraps","Tomaten","Joghurt","Zitrone","Salz","Pfeffer"],
            "tags": ["vegan","schnell"],
            "instructions": [
                "Kichererbsen pürieren, Gewürze & Panko zugeben, Bällchen formen.",
                "Bällchen frittieren oder braten.",
                "Wraps mit Falafel, Tomaten, Joghurtsauce füllen."
            ]
        },
        {
            "id": 15,
            "name": "Gnocchi-Salsiccia-Pfanne",
            "ingredients": ["Kartoffelgnocchi","Salsiccia","Tomaten","Schmand","Oregano","Parmesan","Salz","Pfeffer"],
            "tags": ["mit Fleisch","schnell"],
            "instructions": [
                "Gnocchi in Pfanne braten bis gold.",
                "Salsiccia häuten, zerbröseln, mitbraten.",
                "Tomaten & Schmand unterrühren, würzen.",
                "Mit Parmesan servieren."
            ]
        },
        {
            "id": 16,
            "name": "Brokkoli-Sesam-Stir-Fry",
            "ingredients": ["Brokkoli","Sesamöl","Sojasauce","Knoblauch","Ingwer","Sesam","Frühlingszwiebeln","Chili"],
            "tags": ["asiatisch","vegan","schnell"],
            "instructions": [
                "Sesamöl erhitzen, Knoblauch, Ingwer, Chili anbraten.",
                "Brokkoli zugeben, kurz pfannenrühren.",
                "Mit Sojasauce ablöschen, bissfest garen.",
                "Sesam & Frühlingszwiebeln darüber."
            ]
        },
        {
            "id": 17,
            "name": "Mediterraner Couscous-Salat",
            "ingredients": ["Couscous","Tomaten","Gurke","Schwarze Oliven","Feta","Olivenöl","Zitrone","Petersilie","Salz","Pfeffer"],
            "tags": ["salat","vegetarisch","schnell"],
            "instructions": [
                "Couscous mit heißem Wasser quellen lassen.",
                "Gemüse würfeln, Feta krümeln.",
                "Alles mischen, Dressing aus Öl + Zitrone zufügen.",
                "Mit Petersilie abschmecken."
            ]
        },
        {
            "id": 18,
            "name": "Sahniges Pilz-Risotto",
            "ingredients": ["Risottoreis","Champignons","Zwiebeln","Knoblauch","Butter","Weißwein","Gemüsebrühe","Parmesan","Pfeffer","Salz"],
            "tags": ["vegetarisch","klassisch"],
            "instructions": [
                "Zwiebeln & Knoblauch in Butter glasig dünsten.",
                "Reis zugeben, kurz anschwitzen.",
                "Mit Wein ablöschen, Brühe nach und nach angießen.",
                "Pilze separat anbraten, gegen Ende unterheben.",
                "Parmesan einrühren, cremig rühren, servieren."
            ]
        },
        {
            "id": 19,
            "name": "Pasta Puttanesca",
            "ingredients": ["Spaghetti","Knoblauch","Chili","Tomaten","Schwarze Oliven","Kapern","Anchovis","Petersilie","Olivenöl","Oregano"],
            "tags": ["italienisch","herzhaft"],
            "instructions": [
                "Öl erhitzen, Knoblauch, Chili, Anchovis zerlassen.",
                "Tomaten, Oliven, Kapern, Oregano zugeben, 10 min köcheln.",
                "Spaghetti untermischen, mit Petersilie servieren."
            ]
        },
        {
            "id": 20,
            "name": "Gebratener Reis asiatisch",
            "ingredients": ["Reis","Eier","Karotten","Erbsen","Frühlingszwiebeln","Sojasauce","Sesamöl","Knoblauch","Ingwer"],
            "tags": ["asiatisch","schnell"],
            "instructions": [
                "Reis vorkochen, kalt werden lassen.",
                "Öl erhitzen, Eier zu Rührei braten, herausnehmen.",
                "Gemüse & Aromaten braten, Reis zugeben, würzen.",
                "Eier unterheben, mit Sojasauce abschmecken."
            ]
        },
        {
            "id": 21,
            "name": "Shakshuka",
            "ingredients": ["Eier","Tomaten","Paprika","Zwiebeln","Knoblauch","Chili","Kreuzkümmel","Koriander","Olivenöl","Salz","Pfeffer"],
            "tags": ["vegetarisch","frühstück","herzhaft"],
            "instructions": [
                "Öl erhitzen, Zwiebeln, Paprika, Knoblauch anschwitzen.",
                "Gewürze und Tomaten zufügen, einkochen.",
                "Mulden formen, Eier hineinschlagen, stocken lassen.",
                "Mit Koriander servieren."
            ]
        },
        {
            "id": 22,
            "name": "Spinat-Ricotta-Blätterteig-Taschen",
            "ingredients": ["Blätterteig","Spinat","Ricotta","Knoblauch","Ei","Salz","Pfeffer"],
            "tags": ["vegetarisch","backen","snack"],
            "instructions": [
                "Spinat auftauen, ausdrücken, mit Ricotta & Knoblauch mischen.",
                "Blätterteig zuschneiden, Füllung drauf, zuklappen, andrücken.",
                "Mit verquirltem Ei bestreichen, 20 min 200 °C backen."
            ]
        },
        {
            "id": 23,
            "name": "Pulled-Pork-Wrap",
            "ingredients": ["Pulled Pork","Tortilla Wraps","Coleslaw","BBQ-Sauce"],
            "tags": ["mit Fleisch","schnell"],
            "instructions": [
                "Wraps erwärmen.",
                "Pulled Pork mit BBQ-Sauce mischen.",
                "Mit Coleslaw auf Wrap verteilen, einrollen."
            ]
        },
        {
            "id": 24,
            "name": "Zitronen-Mascarpone-Dessert",
            "ingredients": ["Mascarpone","Lemon Curd","Sahne","Zucker","Vanilleschote","Kekse"],
            "tags": ["sweet","einfach","backen"],
            "instructions": [
                "Sahne schlagen, Mascarpone glatt rühren.",
                "Lemon Curd & Vanille unterheben.",
                "Kekse zerbröseln, abwechselnd mit Creme schichten.",
                "Kalt stellen."
            ]
        },
        {
            "id": 25,
            "name": "Sesam-Hähnchen",
            "ingredients": ["Hähnchenbrust","Sesam","Sojasauce","Honig","Knoblauch","Ingwer","Panko","Ei","Sesamöl","Frühlingszwiebeln"],
            "tags": ["asiatisch","mit Fleisch"],
            "instructions": [
                "Hähnchenstreifen in Ei & Panko-Sesam-Mischung wenden.",
                "Knusprig ausbraten oder backen.",
                "Sauce aus Honig, Sojasauce, Knoblauch, Ingwer erhitzen, Fleisch darin schwenken.",
                "Mit Frühlingszwiebeln servieren."
            ]
        },
        {
            "id": 26,
            "name": "Kartoffel-Lauch-Suppe",
            "ingredients": ["Kartoffeln","Lauch","Zwiebeln","Butter","Gemüsebrühe","Sahne","Salz","Pfeffer"],
            "tags": ["vegetarisch","klassisch","schnell"],
            "instructions": [
                "Butter schmelzen, Zwiebeln & Lauch anschwitzen.",
                "Kartoffelwürfel zugeben, Brühe angießen, 20 min kochen.",
                "Pürieren, Sahne einrühren, würzen."
            ]
        },
        {
            "id": 27,
            "name": "Pesto-Rosso-Gnocchi",
            "ingredients": ["Kartoffelgnocchi","Tomatenmark","Knoblauch","Parmesan","Olivenöl","Kapern","Oregano","Salz","Pfeffer"],
            "tags": ["schnell","vegetarisch"],
            "instructions": [
                "Gnocchi in Pfanne braten.",
                "Tomatenmark mit Öl, Knoblauch, Kapern, Oregano anrühren.",
                "Gnocchi darin schwenken, Parmesan darüber."
            ]
        },
        {
            "id": 28,
            "name": "Caprese-Sandwich",
            "ingredients": ["Vollkornbrot","Tomaten","Mozzarella","Basilikum","Olivenöl","Balsamico","Salz","Pfeffer"],
            "tags": ["vegetarisch","schnell"],
            "instructions": [
                "Brot toasten.",
                "Tomaten & Mozzarella schichten, würzen.",
                "Basilikum, Öl & Balsamico darüber, zusammenklappen."
            ]
        },
        {
            "id": 29,
            "name": "Zimtschnecken",
            "ingredients": ["Hefeteig","Butter","Zimt","Brauner Zucker"],
            "tags": ["sweet","backen"],
            "instructions": [
                "Hefeteig ausrollen, mit Butter bestreichen.",
                "Zucker & Zimt mischen, aufstreuen.",
                "Aufrollen, Scheiben schneiden, 20 min gehen lassen.",
                "20 min bei 180 °C backen."
            ]
        },
        {
            "id": 30,
            "name": "Greek Gyros-Bowls",
            "ingredients": ["Hähnchenbrust","Gyros-Gewürz","Reis","Tomaten","Gurke","Feta","Tzatziki","Olivenöl"],
            "tags": ["mit Fleisch","gesund"],
            "instructions": [
                "Hähnchen in Streifen schneiden, mit Gewürz & Öl marinieren, braten.",
                "Reis kochen.",
                "Gemüse würfeln, Feta zerbröseln.",
                "Alles in Schüssel schichten, Tzatziki darüber."
            ]
        }
    ]
}
# ──────────────────────────────────────────────────────────────────────────────


class RecipeApp(QWidget):
    # ----- Dateien für Portabilität -----
    @property
    def base_dir(self) -> Path:
        if getattr(sys, "frozen", False):
            return Path(sys.executable).parent
        return Path(__file__).parent

    @property
    def fav_path(self) -> Path:
        return self.base_dir / "favourites.json"

    @property
    def shop_path(self) -> Path:
        return self.base_dir / "einkaufsliste.txt"

    # ----- Init -----
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🍲 Rezept-Finder")
        self.resize(1100, 750)

        self.data = DATA
        self.favourites = self.load_favourites()
        self.current_language = "de"

        # ── UI bauen ──────────────────────────────────────────────────────────
        root = QVBoxLayout(self)

        # Kopfzeile
        headline = QLabel("🍲 Rezept-Finder")
        headline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headline.setStyleSheet("font-size:24px;font-weight:bold;")
        root.addWidget(headline)

        # Sprachumschalter
        self.btn_lang = QPushButton("EN")
        self.btn_lang.setFixedWidth(50)
        self.btn_lang.clicked.connect(self.switch_language)
        lang_box = QHBoxLayout()
        lang_box.addStretch()
        lang_box.addWidget(self.btn_lang)
        root.addLayout(lang_box)

        # Suchkriterium & AND-Checkbox
        self.criteria_cmb = QComboBox()
        self.criteria_cmb.addItems(["Nach Zutaten suchen", "Nach Tags suchen"])
        self.chk_match_all = QCheckBox("Alle Zutaten müssen enthalten sein")
        root.addWidget(self.criteria_cmb)
        root.addWidget(self.chk_match_all)

        # Hauptbereich (Zutaten | Rezepte | Tags)
        main = QHBoxLayout()
        root.addLayout(main, stretch=1)

        # Zutaten links (Scroll)
        self.ingredient_cbs = []
        ingr_widget = QWidget()
        ingr_layout = QVBoxLayout(ingr_widget)
        for ing in self.data["ingredients"]:
            cb = QCheckBox(ing)
            self.ingredient_cbs.append(cb)
            ingr_layout.addWidget(cb)
        ingr_layout.addStretch()
        ingr_scroll = QScrollArea()
        ingr_scroll.setWidgetResizable(True)
        ingr_scroll.setWidget(ingr_widget)
        ingr_scroll.setFixedWidth(250)
        main.addWidget(ingr_scroll)

        # Rezeptliste Mitte
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.open_details)
        self.list_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main.addWidget(self.list_widget, stretch=2)

        # Tags rechts (Scroll)
        tag_widget = QWidget()
        tag_layout = QVBoxLayout(tag_widget)
        self.tag_cmb = QComboBox()
        self.tag_cmb.addItem("Alle Tags")
        self.tag_cmb.addItems(self.data["tags"])
        tag_layout.addWidget(QLabel("Tags auswählen:"))
        tag_layout.addWidget(self.tag_cmb)
        tag_layout.addStretch()
        tag_scroll = QScrollArea()
        tag_scroll.setWidgetResizable(True)
        tag_scroll.setWidget(tag_widget)
        tag_scroll.setFixedWidth(220)
        main.addWidget(tag_scroll)

        # Button-Zeile unter Liste
        btns = QHBoxLayout()
        self.btn_search = QPushButton("Suchen")
        self.btn_all = QPushButton("Alle Rezepte")
        self.btn_fav = QPushButton("Favoriten")
        self.btn_ai = QPushButton("KI-Vorschlag")
        btns.addWidget(self.btn_search)
        btns.addWidget(self.btn_all)
        btns.addWidget(self.btn_fav)
        btns.addWidget(self.btn_ai)
        root.addLayout(btns)

        # Detailbereich
        self.detail_label = QLabel()
        self.detail_label.setWordWrap(True)
        self.detail_label.setTextFormat(Qt.TextFormat.RichText)
        self.detail_label.hide()
        root.addWidget(self.detail_label, stretch=1)

        # Detail-Buttons
        det_btns = QHBoxLayout()
        self.btn_back = QPushButton("Zurück")
        self.btn_to_shop = QPushButton("Zur Einkaufsliste")
        self.btn_pdf = QPushButton("Als PDF speichern")
        self.btn_toggle_fav = QPushButton()
        det_btns.addWidget(self.btn_toggle_fav)
        det_btns.addWidget(self.btn_to_shop)
        det_btns.addWidget(self.btn_pdf)
        det_btns.addStretch()
        det_btns.addWidget(self.btn_back)
        root.addLayout(det_btns)
        for b in (self.btn_back, self.btn_toggle_fav, self.btn_to_shop, self.btn_pdf):
            b.hide()

        # ── Signale ──────────────────────────────────────────────────────────
        self.btn_search.clicked.connect(self.search)
        self.btn_all.clicked.connect(self.show_all_recipes)
        self.btn_fav.clicked.connect(self.show_favourites)
        self.btn_ai.clicked.connect(self.ai_suggest)
        self.btn_back.clicked.connect(self.close_details)
        self.btn_toggle_fav.clicked.connect(self.toggle_favourite)
        self.btn_to_shop.clicked.connect(self.add_to_shopping_list)
        self.btn_pdf.clicked.connect(self.save_pdf)

        # Startanzeige
        self.current_recipes = []
        self.current_recipe = None
        self.show_all_recipes()

    # ── Favoriten laden/speichern ────────────────────────────────────────────
    def load_favourites(self):
        if self.fav_path.exists():
            try:
                return set(json.loads(self.fav_path.read_text(encoding="utf-8")))
            except Exception:
                pass
        return set()

    def save_favourites(self):
        try:
            self.fav_path.write_text(json.dumps(list(self.favourites)), encoding="utf-8")
        except Exception as e:
            QMessageBox.warning(self, "Warnung", f"Favoriten konnten nicht gespeichert werden:\n{e}")

    # ── Anzeige-Helpers ──────────────────────────────────────────────────────
    def display_recipes(self, recipes):
        self.list_widget.clear()
        for r in recipes:
            star = "★ " if r["id"] in self.favourites else ""
            item = QListWidgetItem(f"{star}{r['name']}")
            item.setData(Qt.ItemDataRole.UserRole, r)
            self.list_widget.addItem(item)
        self.current_recipes = recipes

    def format_recipe(self, r):
        steps = "<br>".join(f"{i+1}. {s}" for i, s in enumerate(r["instructions"]))
        return (
            f"<h3>{r['name']}</h3>"
            f"<b>Zutaten:</b> {', '.join(r['ingredients'])}<br>"
            f"<b>Tags:</b> {', '.join(r['tags'])}<br><br>"
            f"<b>Anleitung:</b><br>{steps}"
        )

    # ── Such-Logik ───────────────────────────────────────────────────────────
    def search(self):
        if self.criteria_cmb.currentText().startswith("Nach Zutaten"):
            selected = [cb.text() for cb in self.ingredient_cbs if cb.isChecked()]
            if not selected:
                results = []
            elif self.chk_match_all.isChecked():
                results = [r for r in self.data["recipes"] if set(selected).issubset(r["ingredients"])]
            else:
                results = [r for r in self.data["recipes"] if set(r["ingredients"]).intersection(selected)]
        else:
            tag = self.tag_cmb.currentText()
            results = self.data["recipes"] if tag == "Alle Tags" else [r for r in self.data["recipes"] if tag in r["tags"]]

        if not results:
            QMessageBox.information(self, "Keine Treffer", "Keine Rezepte gefunden.")
        self.display_recipes(results)

    # ── Buttons Liste ────────────────────────────────────────────────────────
    def show_all_recipes(self):
        self.display_recipes(self.data["recipes"])

    def show_favourites(self):
        favs = [r for r in self.data["recipes"] if r["id"] in self.favourites]
        if not favs:
            QMessageBox.information(self, "Keine Favoriten", "Noch keine Favoriten markiert.")
        self.display_recipes(favs)

    def ai_suggest(self):
        selected = [cb.text() for cb in self.ingredient_cbs if cb.isChecked()]
        if not selected:
            QMessageBox.information(self, "Hinweis", "Bitte mindestens eine Zutat auswählen.")
            return
        matches = [r for r in self.data["recipes"] if set(r["ingredients"]).intersection(selected)]
        if not matches:
            QMessageBox.information(self, "Keine Vorschläge", "Keine passenden Rezepte gefunden.")
            return
        r = random.choice(matches)
        self.open_details_from_recipe(r)

    # ── Detailansicht ────────────────────────────────────────────────────────
    def open_details(self, item: QListWidgetItem):
        self.open_details_from_recipe(item.data(Qt.ItemDataRole.UserRole))

    def open_details_from_recipe(self, recipe: Dict[str, Any]):
        self.current_recipe = recipe
        self.detail_label.setText(self.format_recipe(recipe))
        self.detail_label.show()
        self.btn_back.show()
        self.btn_toggle_fav.setText("Aus Favoriten entfernen" if recipe["id"] in self.favourites else "Als Favorit markieren")
        self.btn_toggle_fav.show()
        self.btn_to_shop.show()
        self.btn_pdf.show()
        self.list_widget.hide()

    def close_details(self):
        self.detail_label.hide()
        for b in (self.btn_back, self.btn_toggle_fav, self.btn_to_shop, self.btn_pdf):
            b.hide()
        self.list_widget.show()

    # ── Favoriten + Shopping ────────────────────────────────────────────────
    def toggle_favourite(self):
        if not self.current_recipe:
            return
        rid = self.current_recipe["id"]
        if rid in self.favourites:
            self.favourites.remove(rid)
        else:
            self.favourites.add(rid)
        self.save_favourites()
        self.btn_toggle_fav.setText("Aus Favoriten entfernen" if rid in self.favourites else "Als Favorit markieren")
        self.display_recipes(self.current_recipes)

    def add_to_shopping_list(self):
        if not self.current_recipe:
            return
        try:
            with self.shop_path.open("a", encoding="utf-8") as f:
                for ing in self.current_recipe["ingredients"]:
                    f.write(ing + "\n")
            QMessageBox.information(self, "Einkaufsliste", "Zutaten wurden hinzugefügt.")
        except Exception as e:
            QMessageBox.warning(self, "Fehler", f"Konnte nicht schreiben:\n{e}")

    # ── PDF Export ───────────────────────────────────────────────────────────
    def save_pdf(self):
        if not self.current_recipe:
            return
        name = self.current_recipe["name"].replace(" ", "_") + ".pdf"
        file_path, _ = QFileDialog.getSaveFileName(self, "Als PDF speichern", str(self.base_dir / name), "PDF (*.pdf)")
        if not file_path:
            return
        doc = QTextDocument()
        doc.setHtml(self.format_recipe(self.current_recipe))
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(file_path)
        doc.print(printer)
        QMessageBox.information(self, "PDF", f"Gespeichert als:\n{file_path}")

    # ── Sprache wechseln ────────────────────────────────────────────────────
    def switch_language(self):
        self.current_language = "en" if self.current_language == "de" else "de"
        de = self.current_language == "de"
        self.btn_lang.setText("EN" if de else "DE")
        # Minimal: nur Labels, Buttons
        self.criteria_cmb.setItemText(0, "Nach Zutaten suchen" if de else "Search by ingredients")
        self.criteria_cmb.setItemText(1, "Nach Tags suchen" if de else "Search by tags")
        self.chk_match_all.setText("Alle Zutaten müssen enthalten sein" if de else "All ingredients must match")
        self.btn_search.setText("Suchen" if de else "Search")
        self.btn_all.setText("Alle Rezepte" if de else "All recipes")
        self.btn_fav.setText("Favoriten" if de else "Favourites")
        self.btn_ai.setText("KI-Vorschlag" if de else "AI Suggestion")
        self.btn_back.setText("Zurück" if de else "Back")
        self.btn_to_shop.setText("Zur Einkaufsliste" if de else "Add to shopping list")
        self.btn_pdf.setText("Als PDF speichern" if de else "Save as PDF")
        # Tag-Label
        self.tag_cmb.setItemText(0, "Alle Tags" if de else "All tags")

        # Hinweis
        QMessageBox.information(self, "Sprache", "Sprache umgestellt." if de else "Language switched.")

# ── Start ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = RecipeApp()
    win.show()
    sys.exit(app.exec())
