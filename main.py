from pdf2image import convert_from_path
import pytesseract
from PIL import Image


images = convert_from_path("olevel4048mathsyllabus.pdf")

for i, image in enumerate(images):
    text = pytesseract.image_to_string(image)
    print(f"===== Page {i+1} =====")
    print(text)
