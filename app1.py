from ocr import extract_with_pytesseract, extract_with_pdfplumber
from nlp import parse_invoice_data
from save import save_invoice_to_excel
import re
import pytesseract
from PIL import Image
import spacy
import pandas as pd
import time
import os

processed = []
image_path = r"C:\Users\dell\Desktop\BI_prototype\data"
excel_path = r"C:\Users\dell\Desktop\BI_prototype\processed\invoice_data.xlsx"

# Extensions des fichiers pris en charge
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}
PDF_EXTENSION = ".pdf"

while True:
    # Lister tous les fichiers dans le dossier
    files = os.listdir(image_path)
    files = [os.path.join(image_path, file) for file in files]

    for file in files:
        if file not in processed:
            try:
                # Déterminer le type de fichier
                _, ext = os.path.splitext(file)
                ext = ext.lower()  # Extension en minuscule

                if ext in IMAGE_EXTENSIONS:
                    # Traitement des images
                    print(f"Traitement de l'image : {file}")
                    text = extract_with_pytesseract(file)
                elif ext == PDF_EXTENSION:
                    # Traitement des PDFs
                    print(f"Traitement du PDF : {file}")
                    text = extract_with_pdfplumber(file)
                else:
                    print(f"Fichier ignoré (non pris en charge) : {file}")
                    processed.append(file)
                    continue  # Passer au fichier suivant

                # Analyse des données avec NLP
                data = parse_invoice_data(text)

                # Tentative d'enregistrement dans Excel
                while True:
                    try:
                        save_invoice_to_excel(data, excel_path)
                        print("Nouvelles données ajoutées avec succès.")
                        break  # Sortir de la boucle une fois l'enregistrement réussi
                    except PermissionError:
                        print(f"Le fichier {excel_path} est ouvert. Veuillez le fermer pour continuer.")
                        time.sleep(5)  # Attendre 5 secondes avant de réessayer

            except Exception as e:
                print(f"Une erreur est survenue lors du traitement du fichier {file} : {e}")

            processed.append(file)  # Ajouter le fichier à la liste des fichiers traités
