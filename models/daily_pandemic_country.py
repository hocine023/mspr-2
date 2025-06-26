from config_db import connect_to_db

# Fonction pour établir une connexion à la base de données
def connect_to_database():
    return connect_to_db()

# Fonction pour créer la table daily_pandemic_country
def create_daily_pandemic_country_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_pandemic_country (
                    "id_country" INT,
                    "id_pandemic" INT,  
                    "date" DATE,
                    "active_cases" BIGINT,
                    "daily_new_deaths" BIGINT,
                    "daily_new_cases" BIGINT,
                    PRIMARY KEY ("id_country","id_pandemic","date"), 
                    FOREIGN KEY ("id_country") REFERENCES country("id_country") ON DELETE CASCADE,
                    FOREIGN KEY ("id_pandemic") REFERENCES pandemic("id_pandemic") ON DELETE CASCADE
                          
                );
            """)
            conn.commit()
            print("Table daily_pandemic_country vérifiée/créée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création ou vérification de la table daily_pandemic_country : {e}")


# Fonction principale pour exécuter le processus complet
def main():
    # Connexion à la base de données
    conn = connect_to_database()

    # Créer la table daily_pandemic_country
    create_daily_pandemic_country_table(conn)

    # Fermer la connexion
    conn.close()
    print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()
