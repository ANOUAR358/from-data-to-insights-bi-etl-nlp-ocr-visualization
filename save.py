import pandas as pd
import os

def save_invoice_to_excel(data, output_path):
    """
    Enregistre les données d'une facture dans un fichier Excel avec deux tables.
    Si le fichier existe déjà, il vérifie si l'Order ID existe déjà et ajoute les données sinon.
    :param data: Dictionnaire contenant les données structurées de la facture.
    :param output_path: Chemin du fichier Excel de sortie.
    """
    # Préparer les nouvelles données pour l'en-tête (Header)
    header_data = {
        "Order ID": [data['Order ID']],
        "Customer ID": [data['Customer ID']],
        "Order Date": [data['Order Date']],
        "Contact Name": [data['Customer Details'].get('Contact Name')],
        "Address": [data['Customer Details'].get('Address')],
        "City": [data['Customer Details'].get('City')],
        "Postal Code": [data['Customer Details'].get('Postal Code')],
        "Country": [data['Customer Details'].get('Country')],
        "Phone": [data['Customer Details'].get('Phone')],
        "Total Price": [data['Total Price']]
    }
    new_header_df = pd.DataFrame(header_data)

    # Préparer les nouvelles données pour les produits (Products)
    new_products_df = pd.DataFrame(data['Products'])
    new_products_df['Order ID'] = data['Order ID']  # Ajouter l'Order ID pour relier les produits à l'en-tête

    # Si le fichier Excel existe, charger les données existantes
    if os.path.exists(output_path):
        # Charger les feuilles existantes
        existing_header_df = pd.read_excel(output_path, sheet_name="Invoice Header")
        existing_products_df = pd.read_excel(output_path, sheet_name="Product Details")

        # Vérifier si l'Order ID existe déjà
        if data['Order ID'] in existing_header_df['Order ID'].values:
            print(f"L'Order ID {data['Order ID']} existe déjà dans le fichier. Aucune donnée ajoutée.")
            return

        # Ajouter les nouvelles données aux anciennes
        updated_header_df = pd.concat([existing_header_df, new_header_df], ignore_index=True)
        updated_products_df = pd.concat([existing_products_df, new_products_df], ignore_index=True)
    else:
        # Si le fichier n'existe pas, créer de nouvelles tables
        updated_header_df = new_header_df
        updated_products_df = new_products_df

    # Enregistrer les données mises à jour dans le fichier Excel
    with pd.ExcelWriter(output_path, engine='openpyxl', mode='w') as writer:
        updated_header_df.to_excel(writer, index=False, sheet_name="Invoice Header")
        updated_products_df.to_excel(writer, index=False, sheet_name="Product Details")

    print(f"Les données ont été enregistrées avec succès dans {output_path}.")