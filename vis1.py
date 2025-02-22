from flask import Flask
import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import pandas as pd
import os

# Chemin vers le fichier Excel
FILE_PATH = "invoice_data.xlsx"  # Assurez-vous que ce fichier existe

# Initialisation de Flask
server = Flask(__name__)

# Intégration de Dash à Flask
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

# Fonction pour nettoyer les données
def clean_data(df):
    df.rename(columns=lambda x: x.strip(), inplace=True)
    df['Country'] = df['Country'].str.replace('‘', '').str.strip()
    df['Country'] = df['Country'].str.replace('ltaly', 'Italy')
    df['Total Price'] = pd.to_numeric(df['Total Price'], errors='coerce')
    return df

# Fonction pour lire et traiter les données de la première feuille
def read_excel_data(file_path):
    try:
        df = pd.read_excel(file_path, sheet_name=0, engine='openpyxl')
        df = clean_data(df)  # Nettoyer les données

        if 'Country' in df.columns and 'Total Price' in df.columns:
            grouped = df.groupby('Country').agg({
                'Country': 'count',  # Nombre de demandes
                'Total Price': 'sum'  # Somme des prix totaux
            }).rename(columns={
                'Country': 'Nombre de Demandes',
                'Total Price': 'Prix Total'
            })
            grouped.reset_index(inplace=True)
            return grouped
        else:
            raise ValueError("Les colonnes 'Country' et 'Total Price' sont manquantes.")
    except Exception as e:
        print(f"Erreur lors de la lecture des données : {e}")
        return pd.DataFrame(columns=['Country', 'Nombre de Demandes', 'Prix Total'])

# Fonction pour lire et traiter les données de la deuxième feuille
def read_product_data(file_path):
    try:
        df = pd.read_excel(file_path, sheet_name=1, engine='openpyxl')
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
        df['Unit Price'] = pd.to_numeric(df['Unit Price'], errors='coerce')
        df['Total Revenue'] = df['Quantity'] * df['Unit Price']  # Calcul de la rentabilité
        return df
    except Exception as e:
        print(f"Erreur lors de la lecture des données produits : {e}")
        return pd.DataFrame(columns=['Product Name', 'Quantity', 'Total Revenue'])

# Chargement initial des données
initial_data = read_excel_data(FILE_PATH)
product_data = read_product_data(FILE_PATH)

# Données pour les cartes
if not product_data.empty:
    most_sold_product = product_data.groupby('Product Name').sum().sort_values('Quantity', ascending=False).iloc[0]
    most_profitable_product = product_data.groupby('Product Name').sum().sort_values('Total Revenue', ascending=False).iloc[0]
    total_profitability = product_data['Total Revenue'].sum()  # Rentabilité totale
else:
    most_sold_product = {'Product Name': 'Aucun', 'Quantity': 0}
    most_profitable_product = {'Product Name': 'Aucun', 'Total Revenue': 0}
    total_profitability = 0

available_countries = initial_data['Country'].unique() if not initial_data.empty else []

# Disposition de l'application Dash
app.layout = html.Div([
    html.H1("Visualisation des Données", style={'text-align': 'center'}),

    # Cartes pour les produits
    html.Div([
        html.Div([
            html.H3("Produit le plus vendu"),
            html.P(f"{most_sold_product.name} ({most_sold_product['Quantity']} unités)"),
        ], style={'background-color': '#f0f8ff', 'padding': '10px', 'margin': '10px', 'border-radius': '5px'}),
        html.Div([
            html.H3("Produit le plus rentable"),
            html.P(f"{most_profitable_product.name} ({most_profitable_product['Total Revenue']:.2f} €)"),
        ], style={'background-color': '#f8f0ff', 'padding': '10px', 'margin': '10px', 'border-radius': '5px'}),
        html.Div([
            html.H3("Rentabilité Totale"),
            html.P(f"{total_profitability:.2f} €"),  # Affichage de la rentabilité totale
        ], style={'background-color': '#ffebcd', 'padding': '10px', 'margin': '10px', 'border-radius': '5px'}),  # Carte de rentabilité totale
    ], style={'display': 'flex', 'justify-content': 'space-around'}),

    # Filtre pour sélectionner les pays
    html.Div([
        html.Label("Filtrer par Pays :"),
        dcc.Dropdown(
            id='country-filter',
            options=[{'label': country, 'value': country} for country in available_countries],
            multi=True,
            placeholder="Sélectionnez les pays..."
        )
    ], style={'margin-bottom': '20px'}),

    # Deux graphiques côte à côte
    html.Div([
        dcc.Graph(id='graph-nombre-demandes', style={'width': '45%', 'display': 'inline-block'}),
        dcc.Graph(id='graph-prix-total', style={'width': '45%', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),

    dcc.Interval(id='interval-component', interval=5000, n_intervals=0)  # Mise à jour toutes les 5 secondes
])

# Callback pour mettre à jour les graphiques
@app.callback(
    [Output('graph-nombre-demandes', 'figure'),
     Output('graph-prix-total', 'figure')],
    [Input('interval-component', 'n_intervals'),
     Input('country-filter', 'value')]
)
def update_graphs(n, selected_countries):
    data = read_excel_data(FILE_PATH)

    if data.empty:
        empty_fig = {
            "layout": {
                "title": "Pas de données disponibles",
                "xaxis": {"title": "Pays"},
                "yaxis": {"title": "Valeurs"}
            }
        }
        return empty_fig, empty_fig

    if selected_countries:
        data = data[data['Country'].isin(selected_countries)]

    # Création de l'échelle de couleur pour un dégradé
    fig_nombre_demandes = {
        "data": [
            {"x": data['Country'],
             "y": data['Nombre de Demandes'],
             "type": "bar",
             "marker": {"colorscale": "Blues", "color": data['Nombre de Demandes']}}
        ],
        "layout": {"title": "Nombre de Demandes par Pays"}
    }

    fig_prix_total = {
        "data": [
            {"x": data['Country'],
             "y": data['Prix Total'],
             "type": "bar",
             "marker": {"colorscale": "Oranges", "color": data['Prix Total']}}
        ],
        "layout": {"title": "Prix Total par Pays"}
    }

    return fig_nombre_demandes, fig_prix_total

# Point d'entrée Flask
@server.route('/')
def index():
    return "Accédez au tableau de bord ici : <a href='/dashboard/'>Dashboard</a>"

# Lancement du serveur Flask
if __name__ == '__main__':
    if os.path.exists(FILE_PATH):
        server.run(debug=True, host='0.0.0.0', port=8050)
    else:
        print("Le fichier spécifié n'existe pas.")
