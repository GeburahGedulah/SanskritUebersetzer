from PyQt5.QtWidgets import QMainWindow, QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem, QDialog, QLabel, QLineEdit, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from funktionen import translate

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sanskrit Übersetzer")
        self.setGeometry(100, 100, 800, 600)

        self.text_file_path = None
        self.translation = ""

        self.setup_ui()

    def setup_ui(self):
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)

        self.original_text_edit = QTextEdit()
        self.original_text_edit.setReadOnly(True)
        self.original_text_edit.setStyleSheet("background-color: lightgray")

        self.translation_text_edit = QTextEdit()
        self.translation_text_edit.setReadOnly(True)

        load_button = QPushButton("Textdatei laden")
        load_button.clicked.connect(self.load_text_file)

        export_button = QPushButton("Textdatei exportieren")
        export_button.clicked.connect(self.export_text_file)

        translate_button = QPushButton("Übersetzen")
        translate_button.clicked.connect(self.translate_text)

        OCRimport_button = QPushButton("OCR Import")
        OCRimport_button.clicked.connect(self.open_window)

        table_button = QPushButton("Wörter auflisten")
        table_button.clicked.connect(self.show_word_list)

        dictionary_button = QPushButton("Wörterbuch")
        dictionary_button.clicked.connect(self.show_dictionary_dialog)

        main_layout.addWidget(self.original_text_edit)
        main_layout.addWidget(self.translation_text_edit)
        main_layout.addWidget(load_button)
        main_layout.addWidget(export_button)
        main_layout.addWidget(translate_button)
        main_layout.addWidget(table_button)
        main_layout.addWidget(dictionary_button)
        main_layout.addWidget(OCRimport_button)

        self.setCentralWidget(main_widget)

    def load_text_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Textdateien (*.txt)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            try:
                with open(file_path, "r") as file:
                    text = file.read()
                    self.original_text_edit.setPlainText(text)
                    self.text_file_path = file_path
            except Exception as e:
                QMessageBox.critical(self, "Fehler", str(e))

    def export_text_file(self):
        if self.text_file_path is None:
            QMessageBox.warning(self, "Warnung", "Es wurde keine Textdatei geladen.")
            return

        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setDefaultSuffix("txt")
        file_dialog.setNameFilter("Textdateien (*.txt)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            try:
                with open(file_path, "w") as file:
                    file.write(self.translation)
                    QMessageBox.information(self, "Erfolg", "Die Übersetzung wurde erfolgreich exportiert.")
            except Exception as e:
                QMessageBox.critical(self, "Fehler", str(e))

    def translate_text(self):
        original_text = self.original_text_edit.toPlainText()
        self.translation = translate(original_text)

        transliteration = "Transliteration: " + original_text  # Hier können Sie die Transliteration implementieren

        self.translation_text_edit.setPlainText(transliteration + "\n" + self.translation)

    def show_word_list(self):
        original_text = self.original_text_edit.toPlainText()
        words = original_text.split()  # Hier können Sie die Wörterliste entsprechend Ihrer Anforderungen generieren

        table_dialog = QDialog(self)
        table_dialog.setWindowTitle("Wörter auflisten")
        table_dialog.setGeometry(200, 200, 600, 400)
        table_layout = QVBoxLayout(table_dialog)

        table = QTableWidget(len(words), 2, table_dialog)
        table.setHorizontalHeaderLabels(["Devanagari", "Transliteration"])

        for row, word in enumerate(words):
            devanagari_item = QTableWidgetItem(word)
            transliteration_item = QTableWidgetItem("Transliteration")  # Hier können Sie die Transliteration für jedes Wort generieren

            table.setItem(row, 0, devanagari_item)
            table.setItem(row, 1, transliteration_item)

        table_layout.addWidget(table)
        table_dialog.exec_()

    def show_dictionary_dialog(self):
        dictionary_dialog = QDialog(self)
        dictionary_dialog.setWindowTitle("Wörterbuch")
        dictionary_dialog.setGeometry(200, 200, 400, 300)
        dictionary_layout = QGridLayout(dictionary_dialog)

        dictionary_label = QLabel("Wörterbuch:")
        dictionary_line_edit = QLineEdit()
        dictionary_line_edit.setReadOnly(True)
        dictionary_line_edit.setText("Standardwörterbuch")  # Hier können Sie das Standardwörterbuch implementieren

        dictionary_layout.addWidget(dictionary_label, 0, 0)
        dictionary_layout.addWidget(dictionary_line_edit, 0, 1)

        dictionary_dialog.exec_()

    def open_window(self):
        window = QDialog(self)
        window.setWindowTitle("Bild- und Textanzeige")
        window.setGeometry(200, 200, 800, 400)
        window_layout = QHBoxLayout(window)

        image_widget = QLabel(window)
        text_widget = QTextEdit(window)

        window_layout.addWidget(image_widget)
        window_layout.addWidget(text_widget)

        button_layout = QVBoxLayout()

        button_1 = QPushButton("Button 1")
        button_1.clicked.connect(lambda checked, index=1: self.button_clicked(index))
        button_layout.addWidget(button_1)

        button_2 = QPushButton("Button 2")
        button_2.clicked.connect(lambda checked, index=2: self.button_clicked(index))
        button_layout.addWidget(button_2)

        button_3 = QPushButton("Button 3")
        button_3.clicked.connect(lambda checked, index=3: self.button_clicked(index))
        button_layout.addWidget(button_3)

        button_4 = QPushButton("Button 4")
        button_4.clicked.connect(lambda checked, index=4: self.button_clicked(index))
        button_layout.addWidget(button_4)

        button_5 = QPushButton("Button 5")
        button_5.clicked.connect(lambda checked, index=5: self.button_clicked(index))
        button_layout.addWidget(button_5)

        button_6 = QPushButton("Button 6")
        button_6.clicked.connect(lambda checked, index=6: self.button_clicked(index))
        button_layout.addWidget(button_6)

        window_layout.addLayout(button_layout)

        window.exec_()

    def button_clicked(self, index):
        # Hier kommt der Code für die Funktionalität des jeweiligen Buttons
        pass
