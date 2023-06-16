import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem
from indic_transliteration import sanscript

class NounFormGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.input = QLineEdit()
        self.input.setPlaceholderText("Sanskrit-Wort eingeben")
        layout.addWidget(self.input)

        self.translation = QLineEdit()
        self.translation.setPlaceholderText("Deutsche Übersetzung eingeben")
        layout.addWidget(self.translation)

        self.button = QPushButton('Generate Forms')
        layout.addWidget(self.button)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['Grammatische Beschreibung', 'Lateinische Schrift', 'Devanagari', 'Deutsch'])
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.button.clicked.connect(self.on_click)

    def on_click(self):
        noun = self.input.text()
        german_noun = self.translation.text()
        forms = self.generate_forms(noun, german_noun)

        self.table.setRowCount(len(forms))

        for i, form in enumerate(forms):
            for j, cell in enumerate(form):
                self.table.setItem(i, j, QTableWidgetItem(cell))

        # Save forms to a JSON file
        self.save_forms_to_json(forms)

    def generate_forms(self, noun, german_noun):
        # Remove the final 'a' from the noun
        stem = noun[:-1]

        # Define the case endings for singular, dual and plural for masculine, feminine and neuter
        endings = {
            'maskulin': {
                'singular': ['ḥ', '', 'm', 'nā', 'ye', 'āt', 'eḥ', 'au'],
                'dual': ['ī', 'ī', 'ī', 'bhyām', 'bhyām', 'bhyām', 'ī', 'ī'],
                'plural': ['ayaḥ', 'ayaḥ', 'īn', 'bhiḥ', 'bhyāḥ', 'bhyāḥ', 'īnām', 'iṣu']
            },
            'feminin': {
                'singular': ['ā', 'e', 'ām', 'ayā', 'āyai', 'āyāḥ', 'āyāḥ', 'āyām'],
                'dual': ['e', 'e', 'e', 'ābhyām', 'ābhyām', 'ābhyām', 'āyām', 'āyām'],
                'plural': ['āḥ', 'āḥ', 'āḥ', 'ābhiḥ', 'ābhyāḥ', 'ābhyāḥ', 'ānām', 'āsu']
            },
            'neutrum': {
                'singular': ['m', 'm', 'm', 'nā', 'ne', 'nāt', 'neḥ', 'ni'],
                'dual': ['ī', 'ī', 'ī', 'bhyām', 'bhyām', 'bhyām', 'ī', 'ī'],
                'plural': ['āni', 'āni', 'āni', 'bhiḥ', 'bhyāḥ', 'bhyāḥ', 'īnām', 'iṣu']
            }
        }

        german_cases = ['Nominativ', 'Genitiv', 'Dativ', 'Akkusativ']

        german_endings = {
            'singular': {
                'endings': ['', 's', 'm', 'n'],
                'articles': ['das', 'des', 'dem', 'das'],
                'prepositions': ['', 'von', 'zu', 'für']
            },
            'plural': {
                'endings': ['e', 'er', 'en', 'e'],
                'articles': ['die', 'der', 'den', 'die'],
                'prepositions': ['', 'von', 'zu', 'für']
            }
        }

        forms = []

        cases = ['Nominativ', 'Vokativ', 'Akkusativ', 'Instrumental', 'Dativ', 'Ablativ', 'Genitiv', 'Lokativ']

        # Generate the forms for each gender, number and case
        for gender, numbers in endings.items():
            for number, case_endings in numbers.items():
                for idx, ending in enumerate(case_endings):
                    form = stem + ending
                    devanagari_form = sanscript.transliterate(form, sanscript.ITRANS, sanscript.DEVANAGARI)
                    german_form = german_endings['singular']['articles'][idx % 4] + ' ' + german_noun + german_endings['singular']['endings'][idx % 4] + ' ' + german_endings['singular']['prepositions'][idx % 4] if 'singular' in number else german_endings['plural']['articles'][idx % 4] + ' ' + german_noun + german_endings['plural']['endings'][idx % 4] + ' ' + german_endings['plural']['prepositions'][idx % 4]
                    forms.append((f"{gender} {number} {cases[idx]}", form, devanagari_form, german_form))

        return forms

    def save_forms_to_json(self, forms):
        data = []
        for form in forms:
            data.append({
                'Grammatische Beschreibung': form[0],
                'Lateinische Schrift': form[1],
                'Devanagari': form[2],
                'Deutsch': form[3]
            })

        with open('forms.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

app = QApplication([])
generator = NounFormGenerator()
generator.show()
app.exec_()
