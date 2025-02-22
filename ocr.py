import pytesseract
from PIL import Image
import pdfplumber
import easyocr
import PyPDF2
# Define path to tesseract executable if you did not add it to variable path

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Open an image and extract text





def extract_with_pytesseract(image_path):
    """
    Utilise Tesseract OCR pour extraire du texte d'une image.
    :param image_path: Chemin vers l'image.
    :return: Texte brut extrait de l'image.
    """
    try:
        # Ouvrir l'image
        image = Image.open(image_path)
        # Utiliser Tesseract pour extraire le texte
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Erreur lors de l'extraction OCR : {e}")
        return None






#3. Extraction de texte à partir de PDF (en utilisant pdfplumber)

# Ouvrir le fichier PDF
def extract_with_pdfplumber(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        # Extraire le texte de la première page
        page = pdf.pages[0]
        text3 = page.extract_text()
    
    return text3


#3. Extraction de texte à partir de PDF (en utilisant PyPDF2)

# Ouvrir le fichier PDF
def extract_with_pypdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        # Extraire le texte de chaque page
        text2 = ""
        for page in reader.pages:
            text2 += page.extract_text()
    
    return text2


import easyocr

def extract_with_easyocr(image_path):
    # Initialiser l'outil OCR
    reader = easyocr.Reader(['en'])  # Langue : anglais

    # Extraire le texte à partir de l'image
    results = reader.readtext(image_path)

    # Construire une chaîne formatée
    extracted_text = "Texte extrait avec EasyOCR :\n\n"
    
    for result in results:
        print(result[1])
        extracted_text += f"{result[1]}\n"

    return extracted_text
