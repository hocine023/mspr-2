import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath("MSPR"))))
from models.config_db import connect_to_db
import csv

# Fonction pour établir une connexion à la base de données
def connect_to_database():
    return connect_to_db()

# Fonction pour insérer les pays dans la table Country
def insert_countries(conn, file_path):
    try:
        with conn.cursor() as cursor:
            # Lire le fichier CSV
            with open(file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)  
                
                for row in csv_reader:
                    country = row['country']
                    continent_name = row['continent']
                    population = row['population']

                    # Obtenir ID continent 
                    cursor.execute("""SELECT "Id_continent" FROM Continent WHERE "continent" = %s""", (continent_name,))
                    continent_id = cursor.fetchone()

                    if continent_id:
                        continent_id = continent_id[0]
                    else:
                        print(f"Continent '{continent_name}' non trouvé pour le pays '{country}', insertion ignorée.")
                        continue  # Ignorer ce pays si le continent n'existe pas

                    # Préparer la requête d'insertion pour le pays
                    insert_query = """
                        INSERT INTO country (country, population, "Id_continent")
                        VALUES (%s, %s, %s)
                        ON CONFLICT (country) DO NOTHING;
                    """
                    cursor.execute(insert_query, (country, population, continent_id))

            # Commit des changements
            conn.commit()
            print("Pays insérés avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'insertion des pays : {e}")

# Fonction principale pour exécuter le processus complet
def main():
    # Connexion à la base de données
    conn = connect_to_database()

    # Chemin vers le fichier de donnes
    file_path = "../donnes_clean/worldometer_coronavirus_summary_data_clean.csv"

    # Insertion des pays
    insert_countries(conn, file_path)

    # Fermer la connexion
    conn.close()
    print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()
