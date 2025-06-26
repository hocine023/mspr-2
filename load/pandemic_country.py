import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath("MSPR"))))
from models.config_db import connect_to_db
import csv

# Fonction pour établir une connexion à la base de données
def connect_to_database():
    return connect_to_db()

# Fonction pour insérer des données dans la table pandemic_country
def insert_pandemic_country_data(conn, file_path):
    try:
        with conn.cursor() as cursor:
            # Lire le fichier CSV
            with open(file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)  # Utilisation de DictReader pour lire les colonnes
                
                
                for row in csv_reader:
                    country_name = row['country']
                    total_confirmed = row['total_confirmed']
                    total_deaths = row['total_deaths']
                    total_recovered = row['total_recovered']
                    active_cases = row['active_cases']
                    total_tests = row['total_tests']
                    # Récupérer l'ID du country
                    cursor.execute("""SELECT "id_country" FROM country WHERE "country" = %s""", (country_name,))
                    country_id = cursor.fetchone()

                    if country_id:
                        country_id = country_id[0]
                        
                        # Insérer les données uniquement pour Covid-19 (id_pandemic = 1)
                        insert_query = """
                            INSERT INTO pandemic_country (
                                "id_country", "id_pandemic", "total_confirmed", "total_deaths", "total_recovered",
                                "active_cases","total_tests"
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT ("id_country", "id_pandemic") DO NOTHING
                            
                        """
                        cursor.execute(insert_query, (
                            country_id, 1, total_confirmed, total_deaths, total_recovered,
                            active_cases,total_tests
                        ))
                    else:
                        print(f"Pays non trouvé pour les données : {country_name}, insertion ignorée.")
            
            # Commit des changements
            conn.commit()
            print("Données insérées avec succès dans la table pandemic_country pour Covid-19.")
    except Exception as e:
        print(f"Erreur lors de l'insertion des données dans pandemic_country pour Covid-19 : {e}")

# Fonction principale pour exécuter le processus complet
def main():
    # Connexion à la base de données
    conn = connect_to_database()

    # Chemin vers le fichier CSV contenant les données
    file_path ="../donnes_clean/worldometer_coronavirus_summary_data_clean.csv"

    # Insertion des données dans la table pandemic_country pour Covid-19
    insert_pandemic_country_data(conn, file_path)

    # Fermer la connexion
    conn.close()
    print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()
