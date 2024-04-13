import tkinter as tk
from tkinter import filedialog
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import PyPDF2

def extract_text_from_image(image):
    if isinstance(image, Image.Image):
        return pytesseract.image_to_string(image)
    else:
        return pytesseract.image_to_string(Image.open(image))

def convert_pdf_to_images(pdf_path):
    return convert_from_path(pdf_path)

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_unprocessed_pdf(pdf_path):
    images = convert_pdf_to_images(pdf_path)
    text = ""
    for image in images:
        text += extract_text_from_image(image)
    return text

def process_file(file_path):
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        text = extract_text_from_image(Image.open(file_path))
    elif file_path.lower().endswith('.pdf'):
        # 여기서는 OCR 처리가 되었는지 확인 후 적절한 처리를 진행합니다
        try:
            # 먼저 OCR 처리된 PDF로 시도합니다
            text = extract_text_from_pdf(file_path)
            if not text:  # 텍스트 추출이 제대로 되지 않았다면 이미지 변환 시도
                text = extract_text_from_unprocessed_pdf(file_path)
        except Exception as e:
            # OCR 처리된 PDF에서 실패하면 OCR 처리되지 않은 PDF로 간주하고 이미지로 처리
            text = extract_text_from_unprocessed_pdf(file_path)
    elif file_path.lower().endswith('.txt'):
        with open(file_path, 'r') as file:
            text = file.read()
    else:
        text = "Unsupported file type"
    return text

def open_file_dialog():
    root = tk.Tk()
    root.withdraw()  # Tkinter 창을 숨김
    file_path = filedialog.askopenfilename()
    if file_path:
        text = process_file(file_path)
        print("Extracted Text:", text)
    root.destroy()

open_file_dialog()
