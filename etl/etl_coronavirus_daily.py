import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import pandas as pd
import numpy as np
from models.config_db import connect_to_db
from load.daily_pandemic_country import insert_daily_pandemic_country_data


# Extraction
def extract(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Fichier chargé avec succès.")
        return data
    except Exception as e:
        print(f"Erreur lors du chargement : {e}")
        return None

# Transformation
def transform(data):
    try:
        # Nettoyage des noms de pays
        data['country'] = data['country'].str.strip().str.replace(" ", "_")

        # Conversion de la date
        data['date'] = pd.to_datetime(data['date'], errors='coerce')

        # Ajout des colonnes année et mois
        data['year'] = data['date'].dt.year
        data['month'] = data['date'].dt.month

        # Assainissement : convertir en numérique et valeurs positives
        for col in ['daily_new_cases', 'active_cases', 'daily_new_deaths', 'cumulative_total_cases', 'cumulative_total_deaths']:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce').abs()

        # Tri pour le calcul des différences
        data.sort_values(by=['country', 'date'], inplace=True)

        # Estimations par différence
        data['daily_cases_from_cumul'] = data.groupby('country')['cumulative_total_cases'].diff()
        data['daily_deaths_from_cumul'] = data.groupby('country')['cumulative_total_deaths'].diff()

        # Médianes mensuelles
        median_active_mensuelle = data.groupby(['country', 'year', 'month'])['active_cases'].median().reset_index()
        median_active_mensuelle.rename(columns={'active_cases': 'median_active_cases_mensuelle'}, inplace=True)

        median_active_annuelle = data.groupby(['country', 'year'])['active_cases'].median().reset_index()
        median_active_annuelle.rename(columns={'active_cases': 'median_active_cases_annuelle'}, inplace=True)

        median_cases_secours = data.groupby(['country', 'year', 'month'])['daily_cases_from_cumul'].median().reset_index()
        median_cases_secours.rename(columns={'daily_cases_from_cumul': 'median_new_cases_from_cumul'}, inplace=True)

        median_deaths_secours = data.groupby(['country', 'year', 'month'])['daily_deaths_from_cumul'].median().reset_index()
        median_deaths_secours.rename(columns={'daily_deaths_from_cumul': 'median_new_deaths_from_cumul'}, inplace=True)

        # Fusion des médianes
        data = data.merge(median_active_mensuelle, on=['country', 'year', 'month'], how='left')
        data = data.merge(median_active_annuelle, on=['country', 'year'], how='left')
        data = data.merge(median_cases_secours, on=['country', 'year', 'month'], how='left')
        data = data.merge(median_deaths_secours, on=['country', 'year', 'month'], how='left')

        # Colonne combinée de secours
        data['median_active_cases_used'] = data['median_active_cases_mensuelle'] \
            .combine_first(data['median_active_cases_annuelle']) \
            .combine_first(data['median_new_cases_from_cumul'])

        # Remplissage des colonnes principales
        if 'daily_new_cases' in data.columns:
            data['daily_new_cases'] = data['daily_new_cases'].fillna(data['median_new_cases_from_cumul'])
            data['daily_new_cases'] = data['daily_new_cases'].fillna(data['median_active_cases_used'])

        if 'daily_new_deaths' in data.columns:
            data['daily_new_deaths'] = data['daily_new_deaths'].fillna(data['median_new_deaths_from_cumul'])
            data['daily_new_deaths'] = data['daily_new_deaths'].fillna(data['median_new_cases_from_cumul'])

        if 'active_cases' in data.columns:
            data['active_cases'] = data['active_cases'].fillna(data['median_active_cases_used'])

        # Suppression des colonnes temporaires
        data.drop(columns=['year', 'month'], inplace=True)

        # Suppression des colonnes cumulatives
        for col in ['cumulative_total_cases', 'cumulative_total_deaths','median_active_cases_used','median_active_cases_mensuelle','median_active_cases_annuelle','median_new_cases_from_cumul','daily_cases_from_cumul','daily_deaths_from_cumul','median_new_deaths_from_cumul']:
            if col in data.columns:
                data.drop(columns=col, inplace=True)
                print(f"Colonne supprimée : {col}")
        int_cols = ['daily_new_cases', 'daily_new_deaths','active_cases']
        for col in int_cols:
            if col in data.columns:
                data[col] = data[col].astype('int64')
        # Tri final
        data.sort_values(by=['country', 'date'], inplace=True)
        data.reset_index(drop=True, inplace=True)


        print("Transformation terminée avec succes")
        return data

    except Exception as e:
        print(f"Erreur de transformation : {e}")
        return None

# Load
def load(data, output_file):
    try:
        data.to_csv(output_file, index=False)
        print(f"Données enregistrées dans : {output_file}")
        
        conn=connect_to_db()
        insert_daily_pandemic_country_data(conn,output_file,1)
        conn.close()
        
    except Exception as e:
        print(f"Erreur lors de l'enregistrement : {e}")

def process_daily(file_path, output_file):
    raw_data = extract(file_path)
    if raw_data is not None:
        cleaned_data = transform(raw_data)
        if cleaned_data is not None:
            load(cleaned_data, output_file)

# Main
if __name__ == "__main__":
    input_file = "../donnes/worldometer_coronavirus_daily_data.csv"
    output_file = "../donnes_clean/worldometer_coronavirus_daily_data_clean.csv"
    process_daily(input_file, output_file)
