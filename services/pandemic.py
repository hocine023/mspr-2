from models.config_db import connect_to_db

# Récupérer toutes les pandémies
def get_all_pandemics():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM pandemic")
        rows = cursor.fetchall()
        pandemics = [{"id_pandemic": row[0], "name": row[1]} for row in rows]
    conn.close()
    return pandemics

# Ajouter une pandémie sans doublon
def add_pandemic(pandemic_name):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO pandemic (name) 
            VALUES (%s) 
            ON CONFLICT (name) 
            DO NOTHING;
        """, (pandemic_name,))
    conn.commit()
    conn.close()

# Supprimer une pandémie
def delete_pandemic(pandemic_id):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM pandemic WHERE \"id_pandemic\" = %s", (pandemic_id,))
    conn.commit()
    conn.close()

# Mettre à jour une pandémie
def update_pandemic(pandemic_id, pandemic_name):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE pandemic SET name = %s WHERE \"id_pandemic\" = %s", (pandemic_name, pandemic_id))
    conn.commit()
    conn.close()
