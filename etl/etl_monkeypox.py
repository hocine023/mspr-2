import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from models.config_db import connect_to_db
from load.daily_pandemic_country import insert_daily_pandemic_country_data


# --- Extraction ---
def extract(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Fichier chargé avec succès.")
        return data
    except Exception as e:
        print(f"Erreur de chargement : {e}")
        return None

# --- Transformation ---
def transform(data):
    try:
        # Suppression de colonnes inutiles
        cols_to_drop = ['iso_code']
        data.drop(columns=[col for col in cols_to_drop if col in data.columns], inplace=True)

        # Renommage des colonnes
        data.rename(columns={
            'new_cases': 'daily_new_cases',
            'new_deaths': 'daily_new_deaths',
            'location': 'country',
            'total_cases':'active_cases'
        }, inplace=True)

        # Suppression des continents et agrégats globaux
        countries_to_exclude = ["Africa", "Europe", "North America", "South America", "Asia", "World", "Puerto Rico","Oceania"]
        data = data[~data['country'].isin(countries_to_exclude)]

        # Uniformisation des noms de pays
        data['country'] = data['country'].replace({
            "United States": "USA",
            "United Kingdom": "UK",
            "Saint Martin (French part)": "Saint_Martin",
            "Democratic Republic of Congo": "Democratic_Republic_Of_The_Congo",
            "Vietnam": "Viet_Nam",
            "Bosnia and Herzegovina": "Bosnia_And_Herzegovina",
            "Czechia": "Czech_Republic"
        })
        data['country'] = data['country'].str.strip().str.replace(" ", "_")

        # Remplissage des valeurs manquantes par 0 pour les colonnes numériques
        numeric_columns = data.select_dtypes(include='number').columns
        data[numeric_columns] = data[numeric_columns].fillna(0)

        # Suppression des colonnes redondantes (dérivées ou inutiles)
        redundant_cols = [
            'new_cases_smoothed', 'new_deaths_smoothed',
            'new_cases_per_million', 'total_cases_per_million',
            'new_cases_smoothed_per_million', 'new_deaths_per_million',
            'total_deaths_per_million', 'new_deaths_smoothed_per_million'
        ]
        existing_redundant = [col for col in redundant_cols if col in data.columns]
        data.drop(columns=existing_redundant, inplace=True)
        for col in existing_redundant:
            print(f"Colonne supprimée (redondante) : {col}")

        # Conversion en entier pour les compteurs
        int_cols = ['total_cases', 'total_deaths', 'daily_new_cases', 'daily_new_deaths','active_cases']
        for col in int_cols:
            if col in data.columns:
                data[col] = data[col].astype('int64')

        # Tri et index reset
        data.sort_values(by=['country', 'date'], inplace=True)
        data.reset_index(drop=True, inplace=True)

        print("Transformation des données réussie.")
        return data

    except Exception as e:
        print(f"Erreur lors de la transformation : {e}")
        return None

# --- Chargement ---
def load(data, output_file):
    try:
        data.to_csv(output_file, index=False)
        print(f"Données enregistrées dans : {output_file}")
        
        conn=connect_to_db()
        insert_daily_pandemic_country_data(conn,output_file,2)
        conn.close()
    except Exception as e:
        print(f"Erreur lors de l'enregistrement : {e}")
        
def process_monkeypox(file_path, output_file):
    raw_data = extract(file_path)
    if raw_data is not None:
        cleaned_data = transform(raw_data)
        if cleaned_data is not None:
            load(cleaned_data, output_file)

if __name__ == "__main__":
    input_file = "../donnes/owid-monkeypox-data.csv"
    output_file = "../donnes_clean/owid-monkeypox-data_clean.csv"
    process_monkeypox(input_file, output_file)

