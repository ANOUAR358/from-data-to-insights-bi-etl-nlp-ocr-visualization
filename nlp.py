
import re
import spacy 



def parse_invoice_data(text):
    """
    Analyse et structure les données extraites de l'image d'une facture.
    :param text: Texte brut extrait de l'image.
    :return: Dictionnaire contenant les informations organisées.
    """
    data = {}
    
    # Extraction des informations générales
    data['Order ID'] = re.search(r'Order ID:\s*(\d+)', text).group(1)
    data['Customer ID'] = re.search(r'Customer ID:\s*(\w+)', text).group(1)
    data['Order Date'] = re.search(r'Order Date:\s*([\d-]+)', text).group(1)
    
    # Extraction des détails du client
    customer_details = re.search(r'Customer Details:\n(.*?)\nProduct Details:', text, re.S).group(1)
    details_lines = [line.split(':', 1) for line in customer_details.split('\n') if ':' in line]
    data['Customer Details'] = {line[0].strip(): line[1].strip() for line in details_lines}
    
    # Extraction des détails des produits
    product_details = re.findall(r'(\d+)\s+(.*?)\s+(\d+)\s+([\d.]+)', text)
    data['Products'] = [
        {'Product ID': prod[0], 'Product Name': prod[1], 'Quantity': int(prod[2]), 'Unit Price': float(prod[3])}
        for prod in product_details
    ]
    
    # Extraction du prix total
    total_price = re.search(r'TotalPrice\s+([\d.]+)', text)
    data['Total Price'] = float(total_price.group(1)) if total_price else None
    
    return data




import spacy
import re

# Charger le modèle spaCy
nlp = spacy.load("fr_core_news_sm")

def extract_invoice_data_with_nlp(text):
    # Appliquer le NLP spaCy pour analyser le texte
    doc = nlp(text)

    # Extraire les données principales avec des expressions régulières
    order_id = re.search(r"Order ID:\s*(\d+)", text).group(1)
    customer_id = re.search(r"Customer ID:\s*(\w+)", text).group(1)
    order_date = re.search(r"Order Date:\s*([\d-]+)", text).group(1)

    # Extraire les détails du client (en utilisant NER de spaCy)
    customer_details = {}
    customer_details["Contact Name"] = None
    customer_details["Address"] = None
    customer_details["City"] = None
    customer_details["Postal Code"] = None
    customer_details["Country"] = None
    customer_details["Phone"] = None
    customer_details["Fax"] = None

    for ent in doc.ents:
        if ent.label_ == "PERSON" and customer_details["Contact Name"] is None:
            customer_details["Contact Name"] = ent.text
        elif ent.label_ == "GPE" and customer_details["City"] is None:
            customer_details["City"] = ent.text
        elif ent.label_ == "MONEY" and customer_details["Postal Code"] is None:
            customer_details["Postal Code"] = ent.text
        elif ent.label_ == "LOC" and customer_details["Country"] is None:
            customer_details["Country"] = ent.text
        elif "phone" in ent.text.lower() and customer_details["Phone"] is None:
            customer_details["Phone"] = ent.text
        elif "fax" in ent.text.lower() and customer_details["Fax"] is None:
            customer_details["Fax"] = ent.text

    # Extraire les produits
    products_section = re.search(r"Product Details:(.*?)TotalPrice", text, re.DOTALL).group(1)
    product_lines = products_section.strip().split("\n")[1:]  # Ignorer la ligne d'en-tête
    products = []
    for line in product_lines:
        match = re.match(r"(\d+)\s+(.*?)\s+(\d+)\s+([\d.]+)", line)
        if match:
            products.append({
                "Product ID": match.group(1),
                "Product Name": match.group(2).strip(),
                "Quantity": int(match.group(3)),
                "Unit Price": float(match.group(4)),
            })

    # Extraire le prix total
    total_price = float(re.search(r"TotalPrice\s*([\d.]+)", text).group(1))

    # Construire le dictionnaire final
    invoice_data = {
        "Order ID": order_id,
        "Customer ID": customer_id,
        "Order Date": order_date,
        "Customer Details": customer_details,
        "Products": products,
        "Total Price": total_price
    }

    return invoice_data
