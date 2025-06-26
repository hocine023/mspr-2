from config_db import connect_to_db

# Fonction pour établir une connexion à la base de données
def connect_to_database():
    return connect_to_db()

# Fonction pour créer la table pandemic
def create_pandemic_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pandemic (
                    "id_pandemic" SERIAL PRIMARY KEY,
                    "name" VARCHAR(255) NOT NULL UNIQUE                   
                );
            """)
            conn.commit()
            print("Table pandemic vérifiée/créée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création ou vérification de la table pandemic : {e}")


# Fonction principale pour exécuter le processus complet
def main():
    # Connexion à la base de données
    conn = connect_to_database()

    # Créer la table pandemic
    create_pandemic_table(conn)

    # Fermer la connexion
    conn.close()
    print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()
