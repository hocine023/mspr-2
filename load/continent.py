import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath("MSPR"))))
from models.config_db import connect_to_db
import csv

# Fonction pour établir une connexion à la base de données
def connect_to_database():
    return connect_to_db()

# Fonction pour inserrer la table continent
def insert_continents(conn, file_path):
    try:
        with conn.cursor() as cursor:
            # Lire le fichier CSV
            with open(file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)  # Utilisation de DictReader pour lire les colonnes par nom
                continents = [row['continent'] for row in csv_reader]  # Extraire la colonne "continent"

            
            insert_query = """
                INSERT INTO Continent (continent)
                VALUES (%s)
                ON CONFLICT (continent) DO NOTHING;
            """
            # Insérer chaque continent
            for continent in continents:
                cursor.execute(insert_query, (continent,))
            conn.commit()
            print(f" continents insérés avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'insertion des continents : {e}")

# Fonction principale pour exécuter le processus complet
def main():
    # Connexion à la base de données
    conn = connect_to_database()

    # Chemin vers le fichier de donnes
    file_path ="../donnes_clean/worldometer_coronavirus_summary_data_clean.csv"

    # Insertion les continents 
    insert_continents(conn, file_path)

    # Fermer la connexion
    conn.close()
    print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()
