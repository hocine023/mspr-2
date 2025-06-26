from config_db import connect_to_db

# Fonction pour établir une connexion à la base de données
def connect_to_database():
    return connect_to_db()

# Fonction pour créer la table country
def create_country_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS country (
                    "id_country" SERIAL PRIMARY KEY,
                    "country" VARCHAR(255) NOT NULL UNIQUE,
                    "population" BIGINT,   
                    "Id_continent" INT,
                    FOREIGN KEY ("Id_continent") REFERENCES Continent("Id_continent")
                           
                );
            """)
            conn.commit()
            print("Table country vérifiée/créée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création ou vérification de la table country : {e}")



# Fonction principale pour exécuter le processus complet
def main():
    # Connexion à la base de données
    conn = connect_to_database()

    # Créer la table country
    create_country_table(conn)

    # Fermer la connexion
    conn.close()
    print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()
