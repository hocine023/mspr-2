import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath("MSPR"))))
from models.config_db import connect_to_db
import csv

# Fonction pour établir une connexion à la base de données
def connect_to_database():
    return connect_to_db()

# Fonction pour insérer des données dans la table daily_pandemic_country pour Covid-19
def insert_daily_pandemic_country_data(conn, file_path,pandemic_id):
    try:
        with conn.cursor() as cursor:
            # Lire le fichier CSV
            with open(file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)  # Lire le CSV avec les noms de colonnes

                for row in csv_reader:
                    country_name = row['country']
                    date = row['date']
                    active_cases=row['active_cases']
                    daily_new_deaths = row['daily_new_deaths']
                    daily_new_cases = row['daily_new_cases']
                    
                    # Récupérer l'ID du pays correspondant
                    cursor.execute("""SELECT "id_country" FROM country WHERE "country" = %s""", (country_name,))
                    country_id = cursor.fetchone()

                    if country_id:
                        country_id = country_id[0]
                        
                        
                        insert_query = """
                            INSERT INTO daily_pandemic_country (
                                "id_country", "id_pandemic", "date", "daily_new_deaths", "daily_new_cases","active_cases"
                            )
                            VALUES (%s, %s, %s, %s, %s,%s)
                            ON CONFLICT DO NOTHING;                            
                        """
                        cursor.execute(insert_query, (
                            country_id,pandemic_id, date, daily_new_deaths, daily_new_cases,active_cases
                        ))
                    else:
                        print(f"Pays non trouvé pour les données : {country_name}, insertion ignorée.")
            
            # Commit des changements
            conn.commit()
            print("Données insérées avec succès dans la table daily_pandemic_country pour Covid-19 et MPOX.")
    except Exception as e:
        print(f"Erreur lors de l'insertion des données dans daily_pandemic_country pour Covid-19 et MPOX : {e}")

# Fonction principale pour exécuter le processus complet
def main():
    # Connexion à la base de données
    conn = connect_to_database()

    # Chemin vers le fichier de donnes
    covid_file ="../donnes_clean/worldometer_coronavirus_daily_data_clean.csv" 
    MPOX_file ="../donnes_clean/owid-monkeypox-data_clean.csv" 

    # Insertion des données dans la table daily_pandemic_country
    # Insérer les données uniquement pour Covid-19 (id_pandemic = 1)
    insert_daily_pandemic_country_data(conn, covid_file,1)
    # Insérer les données uniquement pour MPOX (id_pandemic = 2)
    insert_daily_pandemic_country_data(conn, MPOX_file,2)

    # Fermer la connexion
    conn.close()
    print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()
