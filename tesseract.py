from PIL import Image
import pytesseract

# Pfad zum Tesseract Binary (Falls benötigt. In vielen Fällen erkennt pytesseract den Pfad automatisch)
# pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Öffne ein Bild
img = Image.open("/home/main/PycharmProjects/pythonProject1/img.jpg")

# Setzen Sie die Sprache auf Hindi (Devanagari-Schrift)
custom_config = r'--oem 3 --psm 6 -l hin'

# OCR-Verarbeitung des Bildes
text = pytesseract.image_to_string(img, config=custom_config)

print(text)
