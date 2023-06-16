import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit, QComboBox
from PyQt5.QtGui import QFont, QPalette, QColor
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense


class RNN_GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RNN Builder")
        self.setGeometry(100, 100, 600, 600)

        self.label = QLabel(self)
        self.label.setText("RNN Builder")
        font = QFont("Arial", 20)
        self.label.setFont(font)
        self.label.setGeometry(200, 10, 200, 50)

        self.input_label = QLabel(self)
        self.input_label.setText("Input Size:")
        self.input_label.setGeometry(30, 80, 100, 30)

        self.input_entry = QLineEdit(self)
        self.input_entry.setGeometry(150, 80, 100, 30)
        self.input_entry.setToolTip("Die Größe der Eingabe (Input) definiert die Dimension der Eingabevektoren. Sie sollte der Größe der Merkmalsvektoren entsprechen, die du in deinem Textübersetzungsszenario verwendest.")

        self.hidden_label = QLabel(self)
        self.hidden_label.setText("Hidden Size:")
        self.hidden_label.setGeometry(30, 120, 100, 30)

        self.hidden_entry = QLineEdit(self)
        self.hidden_entry.setGeometry(150, 120, 100, 30)
        self.hidden_entry.setToolTip("Die versteckte Größe (Hidden Size) definiert die Anzahl der Neuronen im LSTM-Layer. Sie beeinflusst die Kapazität und Lernfähigkeit des Modells. Größere versteckte Größen ermöglichen es dem Modell, komplexere Muster zu erlernen, erfordern jedoch mehr Rechenleistung.")

        self.vocab_label = QLabel(self)
        self.vocab_label.setText("Vocabulary Size:")
        self.vocab_label.setGeometry(30, 160, 120, 30)

        self.vocab_entry = QLineEdit(self)
        self.vocab_entry.setGeometry(150, 160, 100, 30)
        self.vocab_entry.setToolTip("Die Größe des Vokabulars (Vocabulary Size) definiert die Anzahl der eindeutigen Wörter oder Zeichen in deinem Textkorpus. Es wird verwendet, um die Dimension des Embedding-Layers und die Anzahl der Ausgabeneuronen im finalen Dense-Layer festzulegen.")

        self.layers_label = QLabel(self)
        self.layers_label.setText("Anzahl der LSTM-Schichten:")
        self.layers_label.setGeometry(30, 200, 180, 30)

        self.layers_entry = QLineEdit(self)
        self.layers_entry.setGeometry(220, 200, 100, 30)
        self.layers_entry.setToolTip("Die Anzahl der LSTM-Schichten definiert, wie viele LSTM-Schichten in das Modell eingefügt werden sollen. Mehr Schichten können dazu beitragen, komplexere Zusammenhänge zu erfassen, erfordern jedoch mehr Rechenleistung und längere Trainingszeiten.")

        self.dropout_label = QLabel(self)
        self.dropout_label.setText("Dropout-Rate:")
        self.dropout_label.setGeometry(30, 240, 100, 30)

        self.dropout_entry = QLineEdit(self)
        self.dropout_entry.setGeometry(150, 240, 100, 30)
        self.dropout_entry.setToolTip("Die Dropout-Rate definiert den Prozentsatz der Neuronen, die während des Trainings deaktiviert werden, um Overfitting zu reduzieren.")

        self.learning_rate_label = QLabel(self)
        self.learning_rate_label.setText("Lernrate:")
        self.learning_rate_label.setGeometry(30, 280, 100, 30)

        self.learning_rate_entry = QLineEdit(self)
        self.learning_rate_entry.setGeometry(150, 280, 100, 30)
        self.learning_rate_entry.setToolTip("Die Lernrate (Learning Rate) bestimmt die Schrittgröße, mit der das Modell die Gewichte anpasst.")

        self.batch_label = QLabel(self)
        self.batch_label.setText("Batch Size:")
        self.batch_label.setGeometry(30, 320, 100, 30)

        self.batch_entry = QLineEdit(self)
        self.batch_entry.setGeometry(150, 320, 100, 30)
        self.batch_entry.setToolTip("Die Batch-Größe (Batch Size) definiert die Anzahl der Trainingsbeispiele, die in einem Schritt verarbeitet werden.")

        self.epochs_label = QLabel(self)
        self.epochs_label.setText("Anzahl der Epochen:")
        self.epochs_label.setGeometry(30, 360, 140, 30)

        self.epochs_entry = QLineEdit(self)
        self.epochs_entry.setGeometry(180, 360, 100, 30)
        self.epochs_entry.setToolTip("Die Anzahl der Epochen definiert, wie oft das Modell über den gesamten Trainingsdatensatz hinweg trainiert wird.")

        self.optimizer_label = QLabel(self)
        self.optimizer_label.setText("Optimizer:")
        self.optimizer_label.setGeometry(30, 400, 100, 30)

        self.optimizer_combo = QComboBox(self)
        self.optimizer_combo.setGeometry(150, 400, 150, 30)
        self.optimizer_combo.addItem("Adam")
        self.optimizer_combo.addItem("SGD")
        self.optimizer_combo.addItem("RMSprop")
        self.optimizer_combo.setToolTip("Der Optimizer bestimmt, wie das Modell während des Trainings angepasst wird.")
        self.optimizer_combo.currentIndexChanged.connect(self.show_optimizer_help)

        self.loss_label = QLabel(self)
        self.loss_label.setText("Loss:")
        self.loss_label.setGeometry(30, 440, 100, 30)

        self.loss_combo = QComboBox(self)
        self.loss_combo.setGeometry(150, 440, 150, 30)
        self.loss_combo.addItem("SparseCategoricalCrossentropy")
        self.loss_combo.addItem("MeanSquaredError")
        self.loss_combo.addItem("BinaryCrossentropy")
        self.loss_combo.setToolTip("Die Loss-Funktion bestimmt, wie der Unterschied zwischen den Vorhersagen des Modells und den tatsächlichen Werten berechnet wird.")
        self.loss_combo.currentIndexChanged.connect(self.show_loss_help)

        self.create_button = QPushButton(self)
        self.create_button.setText("Create RNN")
        self.create_button.setGeometry(30, 500, 120, 30)
        self.create_button.clicked.connect(self.create_rnn)

        self.data_button = QPushButton(self)
        self.data_button.setText("Daten aufbereiten")
        self.data_button.setGeometry(160, 500, 150, 30)
        self.data_button.clicked.connect(self.open_data_window)

    def show_optimizer_help(self):
        optimizer = self.optimizer_combo.currentText()
        help_text = ""
        if optimizer == "Adam":
            help_text = "Adam ist ein adaptiver Optimizer, der häufig für das Training neuronaler Netzwerke verwendet wird. Er kombiniert die Vorteile des AdaGrad-Optimizers und des RMSprop-Optimizers, um eine effiziente Anpassung der Lernrate zu erreichen.\n\nVorteile:\n- Gut geeignet für Textübersetzungsaufgaben\n- Effiziente Anpassung der Lernrate\n\nNachteile:\n- Möglicherweise nicht immer die beste Wahl für alle Probleme"
        elif optimizer == "SGD":
            help_text = "Stochastic Gradient Descent (SGD) ist ein klassischer Optimizer für das Training neuronaler Netzwerke. Er aktualisiert die Gewichte basierend auf dem Gradienten der Verlustfunktion unter Verwendung einer festen Lernrate.\n\nVorteile:\n- Einfach und schnell\n- Funktioniert gut für einfache Modelle\n\nNachteile:\n- Kann langsamer sein als adaptivere Optimizer wie Adam"
        elif optimizer == "RMSprop":
            help_text = "RMSprop ist ein Optimizer, der adaptiv die Lernrate für jedes Gewicht im Modell anpasst. Er ist besonders nützlich, wenn die Verlustfunktion in verschiedene Richtungen unterschiedlich steil ist.\n\nVorteile:\n- Gute Wahl für RNN-Modelle\n- Effektive Anpassung der Lernrate\n\nNachteile:\n- Möglicherweise nicht immer die beste Wahl für alle Probleme"

        self.optimizer_combo.setToolTip(help_text)

    def show_loss_help(self):
        loss = self.loss_combo.currentText()
        help_text = ""
        if loss == "SparseCategoricalCrossentropy":
            help_text = "Sparse Categorical Crossentropy ist eine Verlustfunktion, die häufig bei Multi-Class-Klassifikationsproblemen verwendet wird. Sie wird verwendet, wenn die Zielvariablen als ganze Zahlen kodiert sind, anstatt als One-Hot-Vektoren.\n\nVorteile:\n- Gut geeignet für Textübersetzungsaufgaben\n- Einfache Handhabung von Ganzzahlen als Zielvariablen\n\nNachteile:\n- Kann langsam sein bei großen Vokabularen"
        elif loss == "MeanSquaredError":
            help_text = "Mean Squared Error (MSE) ist eine Verlustfunktion, die häufig bei Regressionsproblemen verwendet wird. Sie misst den mittleren quadratischen Fehler zwischen den Vorhersagen und den tatsächlichen Werten.\n\nVorteile:\n- Gut geeignet für Regressionsprobleme\n- Einfache Handhabung von kontinuierlichen Zielvariablen\n\nNachteile:\n- Kann Probleme mit Ausreißern haben"
        elif loss == "BinaryCrossentropy":
            help_text = "Binary Crossentropy ist eine Verlustfunktion, die häufig bei Binärklassifikationsproblemen verwendet wird. Sie wird verwendet, wenn die Zielvariablen binär sind (z.B. 0 oder 1).\n\nVorteile:\n- Gut geeignet für Binärklassifikationsprobleme\n- Einfache Handhabung von binären Zielvariablen\n\nNachteile:\n- Kann langsam sein bei großen Vokabularen"

        self.loss_combo.setToolTip(help_text)

    def create_rnn(self):
        try:
            input_size = int(self.input_entry.text())
            hidden_size = int(self.hidden_entry.text())
            vocab_size = int(self.vocab_entry.text())
            num_layers = int(self.layers_entry.text())
            dropout_rate = float(self.dropout_entry.text())
            learning_rate = float(self.learning_rate_entry.text())
            batch_size = int(self.batch_entry.text())
            epochs = int(self.epochs_entry.text())
            optimizer = self.optimizer_combo.currentText()
            loss = self.loss_combo.currentText()

            # Erstellen des RNN-Modells
            model = Sequential()
            model.add(Embedding(vocab_size, input_size))
            for _ in range(num_layers):
                model.add(LSTM(hidden_size, dropout=dropout_rate, return_sequences=True))
            model.add(LSTM(hidden_size, dropout=dropout_rate))
            model.add(Dense(vocab_size, activation='softmax'))

            # Kompilieren des Modells
            loss_func = getattr(tf.keras.losses, loss)()
            optimizer_func = getattr(tf.keras.optimizers, optimizer)(learning_rate=learning_rate)
            model.compile(loss=loss_func, optimizer=optimizer_func, metrics=['accuracy'])

            QMessageBox.information(self, "Erfolg", "RNN erfolgreich erstellt und kompiliert!")
        except ValueError:
            QMessageBox.critical(self, "Fehler", "Bitte gib gültige Werte für die Eingabeparameter ein.")

    def open_data_window(self):
        data_window = DataWindow(self)
        data_window.show()


class DataWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Daten aufbereiten")
        self.setGeometry(100, 100, 600, 600)

        self.data_label = QLabel(self)
        self.data_label.setText("Daten eingeben:")
        self.data_label.setGeometry(30, 80, 100, 30)

        self.data_text = QTextEdit(self)
        self.data_text.setGeometry(30, 120, 400, 250)

        self.help_button = QPushButton(self)
        self.help_button.setText("Hilfe")
        self.help_button.setGeometry(30, 400, 80, 30)
        self.help_button.clicked.connect(self.show_data_help)

        self.process_button = QPushButton(self)
        self.process_button.setText("Daten verarbeiten")
        self.process_button.setGeometry(120, 400, 150, 30)
        self.process_button.clicked.connect(self.process_data)

    def show_data_help(self):
        help_text = "Gib hier deine Daten ein, die du für das Training oder die Vorhersage verwenden möchtest. Die Daten sollten in einem geeigneten Format vorliegen, " \
                    "abhängig von deinem spezifischen Textübersetzungsszenario. Du kannst Sätze, Absätze oder Textdokumente eingeben, die in der gewünschten " \
                    "Sprachkombination übersetzt werden sollen.\n\nBeispiel:\n- Quellsprache (Deutsch): 'Das ist ein Beispiel.'\n- Zielsprache (Englisch): 'This is an example.'"
        QMessageBox.information(self, "Hilfe - Daten eingeben", help_text)

    def process_data(self):
        # Hier kannst du den Code zum Aufbereiten der Daten einfügen
        # Du kannst die 'data_text.toPlainText()' verwenden, um auf die eingegebenen Daten zuzugreifen
        QMessageBox.information(self, "Datenverarbeitung", "Daten wurden erfolgreich verarbeitet!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    rnn_gui = RNN_GUI()
    rnn_gui.show()
    sys.exit(app.exec_())
