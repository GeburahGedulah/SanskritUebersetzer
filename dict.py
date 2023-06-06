import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QListWidget, QMessageBox, QInputDialog, QListWidgetItem, QTextEdit
from indic_transliteration import sanscript

class DictionaryApp(QWidget):

    def __init__(self):
        super().__init__()

        self.dictionary_file = 'dictionary.json'

        self.setWindowTitle('Wörterbuch App')
        self.setLayout(QVBoxLayout())

        self.line_word = QLineEdit(self)
        self.line_word.setPlaceholderText("Geben Sie das Wort ein")
        self.layout().addWidget(self.line_word)

        self.line_translation = QLineEdit(self)
        self.line_translation.setPlaceholderText("Geben Sie die Übersetzung ein")
        self.layout().addWidget(self.line_translation)

        self.list_words = QListWidget(self)
        self.list_words.itemClicked.connect(self.item_clicked)
        self.layout().addWidget(self.list_words)

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
        if word and translation:
            dictionary = self.load_dictionary()
            dictionary[word] = translation
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
            translation = dictionary.get(word)
            if translation:
                new_word, ok = QInputDialog.getText(self, "Neues Wort", f"Geben Sie das neue Wort ein:", QLineEdit.Normal, word)
                new_translation, ok = QInputDialog.getText(self, "Neue Übersetzung", f"Geben Sie die neue Übersetzung ein:", QLineEdit.Normal, translation)
                if ok and new_word and new_translation:
                    del dictionary[word]
                    dictionary[new_word] = new_translation
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
        translation = dictionary.get(word, "")
        self.line_translation.setText(translation)
        self.text_display.setText(f"{word} - {self.transliterate(word) if self.is_devanagari(word) else ''} - {translation}")

    def is_devanagari(self, word):
        return all(u'\u0900' <= c <= u'\u097F' for c in word)

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


app = QApplication([])
window = DictionaryApp()
window.show()
app.exec_()
