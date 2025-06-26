import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath("MSPR"))))
from models.config_db import connect_to_db

# Fonction pour établir une connexion à la base de données
def connect_to_database():
    return connect_to_db()

# Fonction pour insérer les pandémies dans la table pandemic
def insert_pandemics(conn):
    try:
        with conn.cursor() as cursor:
            # Les pandémies à insérer
            pandemics = ['COVID-19', 'MPOX']
            
            for pandemic in pandemics:
                insert_query = """
                    INSERT INTO pandemic (name)
                    VALUES (%s)
                    ON CONFLICT ("name")
                    DO NOTHING        
                """
                cursor.execute(insert_query, (pandemic,))

            # Commit des changements
            conn.commit()
            print("Pandémies insérées avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'insertion des pandémies : {e}")

# Fonction principale pour exécuter le processus complet
def main():
    # Connexion à la base de données
    conn = connect_to_database()

    # Insérer les pandémies
    insert_pandemics(conn)

    # Fermer la connexion
    conn.close()
    print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()
