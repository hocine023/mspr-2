import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import numpy as np
from models.config_db import connect_to_db
from load.continent import insert_continents
from load.country import insert_countries
from load.pandemic import insert_pandemics
from load.pandemic_country import insert_pandemic_country_data

def extract(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Extraction réussie.")
        return data
    except Exception as e:
        print(f"Erreur d'extraction : {e}")
        return None


def impute_total_deaths(data):
    if {'total_confirmed', 'total_deaths'}.issubset(data.columns):
        missing_mask = data['total_deaths'].isna() & data['total_confirmed'].notna()
        for index in data[missing_mask].index:
            confirmed = data.loc[index, 'total_confirmed']
            similar = data[
                (data['total_confirmed'].between(confirmed * 0.9, confirmed * 1.1)) &
                (data['total_deaths'].notna())
            ]
            if not similar.empty:
                data.at[index, 'total_deaths'] = similar['total_deaths'].median()
            else:
                global_rate = (data['total_deaths'] / data['total_confirmed']).median()
                data.at[index, 'total_deaths'] = int(confirmed * global_rate)
        print(f"total_deaths imputé pour {missing_mask.sum()} lignes.")
    return data

def impute_total_recovered(data):
    if {'total_confirmed', 'total_deaths', 'total_recovered'}.issubset(data.columns):
        mask = data['total_recovered'].isna() & data['total_confirmed'].notna() & data['total_deaths'].notna()
        data.loc[mask, 'total_recovered'] = data['total_confirmed'] - data['total_deaths']
        print(f"total_recovered imputé pour {mask.sum()} lignes.")
    return data

def correct_active_cases(data):
    if {'total_confirmed', 'total_deaths', 'total_recovered'}.issubset(data.columns):
        data['active_cases'] = data['total_confirmed'] - (data['total_deaths'] + data['total_recovered'])
        print("active_cases recalculé.")
    return data

def impute_total_tests(data):
    if {'total_tests', 'population'}.issubset(data.columns):
        mask = data['total_tests'].isna() & data['population'].notna()
        valid = data[data['total_tests'].notna() & data['population'].notna()]
        tests_per_person = (valid['total_tests'] / valid['population']).median()
        data.loc[mask, 'total_tests'] = data['population'] * tests_per_person
        print(f"total_tests imputé pour {mask.sum()} lignes.")
    return data

# --- Suppression des colonnes redondantes ---
def drop_redundant_columns(data):
    cols_to_drop = [
        'total_cases_per_1m_population',
        'total_deaths_per_1m_population',
        'total_tests_per_1m_population',
        'serious_or_critical'
    ]
    existing_cols = [col for col in cols_to_drop if col in data.columns]
    data.drop(columns=existing_cols, inplace=True)
    if existing_cols:
        print(f"Colonnes supprimées : {existing_cols}")
    return data





def transform(data):
    try:
        data['country'] = data['country'].str.replace(" ", "_")
        data['continent'] = data['continent'].str.replace(" ", "_")
    

       
        data = impute_total_deaths(data)
        data = impute_total_recovered(data)
        data = correct_active_cases(data)
        data = impute_total_tests(data)
        data = drop_redundant_columns(data)

        numeric_columns = [
           'total_confirmed', 'total_deaths', 'total_recovered',
           'active_cases', 'total_tests', 'population'
        ]
        for col in numeric_columns:
            if col in data.columns:
                 data[col] = pd.to_numeric(data[col], errors='coerce').astype('int64')

        print("Transformation terminée.")
        return data
    except Exception as e:
        print(f"Erreur de transformation : {e}")
        return None

def load(data, output_file):
    try:
        data.to_csv(output_file, index=False)
        print(f"Données sauvegardées dans : {output_file}")
        conn=connect_to_db()
        insert_continents(conn, output_file)
        insert_countries(conn,output_file)
        insert_pandemics(conn)
        insert_pandemic_country_data(conn,output_file)
        conn.close()
        
        
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

def process_summary(file_path, output_file):
    raw_data = extract(file_path)
    if raw_data is not None:
        cleaned_data = transform(raw_data)
        if cleaned_data is not None:
            load(cleaned_data, output_file)


if __name__ == "__main__":
    file_path = "../donnes/worldometer_coronavirus_summary_data.csv"
    output_file = "../donnes_clean/worldometer_coronavirus_summary_data_clean.csv"
    process_summary(file_path, output_file)
    
