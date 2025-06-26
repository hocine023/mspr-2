from models.config_db import connect_to_db

# Récupérer tous les continents
def get_all_continents():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Continent")
        rows = cursor.fetchall()
        continents = [{"id": row[0], "continent": row[1]} for row in rows]
    conn.close()
    return continents

# Ajouter un continent sans doublon
def add_continent(continent_name):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Continent (continent) 
            VALUES (%s) 
            ON CONFLICT (continent) 
            DO NOTHING;
        """, (continent_name,))
    conn.commit()
    conn.close()

# Supprimer un continent
def delete_continent(continent_id):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM Continent WHERE \"Id_continent\" = %s", (continent_id,))
    conn.commit()
    conn.close()

# Mettre à jour un continent
def update_continent(continent_id, continent_name):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE Continent SET continent = %s WHERE  \"Id_continent\" = %s", (continent_name, continent_id))
    conn.commit()
    conn.close()
