import json
from PyQt5.QtCore import Qt, QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QListWidget, QMessageBox,
                             QInputDialog, QListWidgetItem, QTextEdit, QDialog, QComboBox, QLabel)
from indic_transliteration import sanscript

class DictionaryApp(QDialog):

    def __init__(self):
        super().__init__()

        self.dictionary_file = 'dictionary.json'

        self.setWindowTitle('Wörterbuch App')
        self.setLayout(QVBoxLayout())

        self.line_word = QLineEdit(self)
        self.line_word.setPlaceholderText("Geben Sie das Wort ein")
        devanagari_regex = QRegularExpression(u'[\u0900-\u097F\s]*')
        validator = QRegularExpressionValidator(devanagari_regex, self.line_word)
        self.line_word.setValidator(validator)
        self.layout().addWidget(self.line_word)

        self.line_translation = QLineEdit(self)
        self.line_translation.setPlaceholderText("Geben Sie die Übersetzung ein")
        self.layout().addWidget(self.line_translation)

        self.combo_type = QComboBox(self)
        self.combo_type.addItems(['Nomen', 'Verb', 'Unveränderliches', 'Präposition'])
        self.layout().addWidget(self.combo_type)

        self.line_comment = QLineEdit(self)
        self.line_comment.setPlaceholderText("Geben Sie einen Kommentar ein")
        self.layout().addWidget(self.line_comment)

        self.list_words = QListWidget(self)
        self.list_words.itemClicked.connect(self.item_clicked)
        self.layout().addWidget(self.list_words)

        self.line_search = QLineEdit(self)
        self.line_search.setPlaceholderText("Suche...")
        self.line_search.textChanged.connect(self.search_word)
        self.layout().addWidget(self.line_search)

        self.button_add = QPushButton('Wort hinzufügen', self)
        self.button_add.clicked.connect(self.add_word)
        self.layout().addWidget(self.button_add)

        self.button_edit = QPushButton('Eintrag bearbeiten', self)
        self.button_edit.clicked.connect(self.edit_entry)
        self.layout().addWidget(self.button_edit)

        self.button_delete = QPushButton('Eintrag löschen', self)
        self.button_delete.clicked.connect(self.delete_entry)
        self.layout().addWidget(self.button_delete)

        self.text_display = QTextEdit(self)
        self.text_display.setReadOnly(True)
        self.layout().addWidget(self.text_display)

        self.load_words()

    def transliterate(self, word):
        return sanscript.transliterate(word, sanscript.DEVANAGARI, sanscript.IAST)

    def add_word(self):
        word = self.line_word.text()
        translation = self.line_translation.text()
        word_type = self.combo_type.currentText()
        comment = self.line_comment.text()

        if word and translation:
            dictionary = self.load_dictionary()
            dictionary[word] = {'translation': translation, 'type': word_type, 'comment': comment}
            self.save_dictionary(dictionary)

            self.list_words.addItem(word)
            QMessageBox.information(self, "Erfolg", "Wort wurde erfolgreich hinzugefügt.")
        else:
            QMessageBox.warning(self, "Fehler", "Bitte geben Sie sowohl Wort als auch Übersetzung ein.")

    def edit_entry(self):
        item = self.list_words.currentItem()
        if item:
            word = item.text()
            dictionary = self.load_dictionary()
            entry = dictionary.get(word)
            if entry:
                new_word, ok = QInputDialog.getText(self, "Neues Wort", f"Geben Sie das neue Wort ein:", QLineEdit.Normal, word)
                new_translation, ok = QInputDialog.getText(self, "Neue Übersetzung", f"Geben Sie die neue Übersetzung ein:", QLineEdit.Normal, entry['translation'])
                new_type, ok = QInputDialog.getItem(self, "Wortart", f"Wählen Sie die Wortart aus:", ['Nomen', 'Verb', 'Unveränderliches', 'Präposition'], 0, False)
                new_comment, ok = QInputDialog.getText(self, "Neuer Kommentar", f"Geben Sie einen neuen Kommentar ein:", QLineEdit.Normal, entry['comment'])
                if ok and new_word and new_translation:
                    del dictionary[word]
                    dictionary[new_word] = {'translation': new_translation, 'type': new_type, 'comment': new_comment}
                    self.save_dictionary(dictionary)

                    item.setText(new_word)
                    QMessageBox.information(self, "Erfolg", "Der Eintrag wurde erfolgreich geändert.")
            else:
                QMessageBox.warning(self, "Fehler", f"Keine Übersetzung für {word} gefunden.")
        else:
            QMessageBox.warning(self, "Fehler", "Bitte wählen Sie ein Wort aus der Liste aus.")

    def delete_entry(self):
        item = self.list_words.currentItem()
        if item:
            word = item.text()
            dictionary = self.load_dictionary()
            if word in dictionary:
                del dictionary[word]
                self.save_dictionary(dictionary)

                self.list_words.takeItem(self.list_words.row(item))
                QMessageBox.information(self, "Erfolg", "Das Wort wurde erfolgreich gelöscht.")
            else:
                QMessageBox.warning(self, "Fehler", f"Das Wort {word} wurde nicht im Wörterbuch gefunden.")
        else:
            QMessageBox.warning(self, "Fehler", "Bitte wählen Sie ein Wort aus der Liste aus.")

    def item_clicked(self, item: QListWidgetItem):
        word = item.text()
        self.line_word.setText(word)
        dictionary = self.load_dictionary()
        entry = dictionary.get(word, {"translation": "", "type": "", "comment": ""})
        translation = entry.get("translation", "")
        word_type = entry.get("type", "")
        comment = entry.get("comment", "")
        self.line_translation.setText(translation)
        self.combo_type.setCurrentText(word_type if word_type else 'Nomen')
        self.line_comment.setText(comment)
        self.text_display.setText(f"{word} - {self.transliterate(word) if self.is_devanagari(word) else ''} - {translation} - {word_type} - {comment}")

    def is_devanagari(self, word):
        return all(u'\u0900' <= c <= u'\u097F' for c in word)

    def search_word(self):
        search_text = self.line_search.text()
        dictionary = self.load_dictionary()
        for word, entry in dictionary.items():
            if search_text in word or search_text in self.transliterate(word) or search_text in entry.get('translation', ''):
                self.list_words.addItem(word)
            else:
                list_items = self.list_words.findItems(word, Qt.MatchExactly)
                if list_items:
                    for item in list_items:
                        self.list_words.takeItem(self.list_words.row(item))

    def load_dictionary(self):
        try:
            with open(self.dictionary_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_dictionary(self, dictionary):
        with open(self.dictionary_file, 'w') as f:
            json.dump(dictionary, f)

    def load_words(self):
        dictionary = self.load_dictionary()
        for word in dictionary.keys():
            self.list_words.addItem(word)

def start_dictionary_app():
    dialog = DictionaryApp()
    dialog.exec_()

def process_forms():
    dictionary = {}
    with open('forms.json', 'r') as f:
        forms = json.load(f)
    for form in forms:
        word = form['Lateinische Schrift']
        dictionary[word] = {
            'translation': form['Deutsch'],
            'type': 'Nomen',
            'comment': form['Grammatische Beschreibung']
        }
    with open('dictionary.json', 'w') as f:
        json.dump(dictionary, f)

if __name__ == "__main__":
    process_forms()
    app = QApplication([])
    start_dictionary_app()
