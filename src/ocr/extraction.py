from pytesseract import image_to_string
from src.ocr.image_processing import preprocess_image
from PIL import Image
import cv2

def extract_text_from_image(image_path:str, language:str = None)-> str:
    img_array = cv2.imread(image_path)
    img_array = preprocess_image(img_array)
    image = Image.fromarray(img_array)
    text = image_to_string(image, lang=language,config='--psm 1 --oem 1')
    print("OCR done: language: ", language)
    return text
