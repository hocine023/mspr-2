from continent import create_continent_table
from country import create_country_table
from pandemic import create_pandemic_table
from pandemic_country import create_pandemic_country_table
from daily_pandemic_country import create_daily_pandemic_country_table

from config_db import connect_to_db

def main():
    conn = connect_to_db()

    # Création des tables dans l'ordre correct (relations FK respectées)
    create_continent_table(conn)
    create_country_table(conn)
    create_pandemic_table(conn)
    create_pandemic_country_table(conn)
    create_daily_pandemic_country_table(conn)

    conn.close()
    print("Toutes les tables ont été créées avec succès.")

if __name__ == "__main__":
    main()
