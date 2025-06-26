from models.config_db import connect_to_db

# Récupérer toutes les données de pandémie par pays
def get_all_pandemic_country():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM pandemic_country")
        rows = cursor.fetchall()
        pandemic_countries = [{
            "id_country": row[0],
            "id_pandemic": row[1],
            "total_confirmed": row[2],
            "total_deaths": row[3],
            "total_recovered": row[4],
            "active_cases": row[5],
            "total_tests": row[6]

        } for row in rows]
    conn.close()
    return pandemic_countries

# Récupérer les données de pandémie par pays et id_pandemic
def get_pandemic_country_by_id(id_country, id_pandemic):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM pandemic_country 
            WHERE "id_country" = %s AND "id_pandemic" = %s
        """, (id_country, id_pandemic))
        row = cursor.fetchone()
        if row:
            pandemic_country = {
                "id_country": row[0],
                "id_pandemic": row[1],
                "total_confirmed": row[2],
                "total_deaths": row[3],
                "total_recovered": row[4],
                "active_cases": row[5],
                "total_tests": row[6]

            }
            return pandemic_country
        return None
def get_cases_by_continent():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT 
                c.continent, 
                SUM(p."total_confirmed") AS total_confirmed,
                SUM(p."total_deaths") AS total_deaths,
                SUM(p."total_recovered") AS total_recovered
            FROM pandemic_country p
            JOIN Country co ON p."id_country" = co."id_country"
            JOIN Continent c ON co."Id_continent" = c."Id_continent"
            WHERE p."id_pandemic" = 1
            GROUP BY c.continent
            ORDER BY total_confirmed DESC   
        """)
        rows = cursor.fetchall()
        continent_cases = [{
            "continent": row[0],
            "total_confirmed": row[1],
            "total_deaths": row[2],
            "total_recovered": row[3]
        } for row in rows]
    return continent_cases



# Ajouter une entrée pour un pays et une pandémie
def add_pandemic_country(id_country, id_pandemic, total_confirmed, total_deaths, total_recovered,
                         active_cases,total_tests):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO pandemic_country (
                    "id_country", "id_pandemic", "total_confirmed", "total_deaths", "total_recovered", 
                    "active_cases", "total_tests"
                ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT ("id_country", "id_pandemic") DO NOTHING
                
            """, (id_country, id_pandemic, total_confirmed, total_deaths, total_recovered,
                  active_cases,total_tests))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de l'ajout de la pandémie pour le pays : {e}")
    finally:
        conn.close()

# Supprimer une entrée pour un pays et une pandémie
def delete_pandemic_country(id_country, id_pandemic):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM pandemic_country WHERE "id_country" = %s AND "id_pandemic" = %s
            """, (id_country, id_pandemic))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la suppression de la pandémie pour le pays : {e}")
    finally:
        conn.close()

# Mettre à jour les données d'une pandémie pour un pays
def update_pandemic_country(id_country, id_pandemic, total_confirmed, total_deaths, total_recovered,
                            active_cases,total_tests):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE pandemic_country
                SET 
                    "total_confirmed" = %s, 
                    "total_deaths" = %s, 
                    "total_recovered" = %s, 
                    "active_cases" = %s,  
                    "total_tests" = %s
                WHERE "id_country" = %s AND "id_pandemic" = %s
            """, (total_confirmed, total_deaths, total_recovered, active_cases,
                  total_tests,id_country, id_pandemic))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la mise à jour de la pandémie pour le pays : {e}")
    finally:
        conn.close()
