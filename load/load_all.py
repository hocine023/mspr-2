import os
import sys

# S'assurer que les modules du même dossier peuvent être importés
sys.path.append(os.path.dirname(__file__))

from continent import main as load_continent
from country import main as load_country
from pandemic import main as load_pandemic
from pandemic_country import main as load_pandemic_country
from daily_pandemic_country import main as load_daily_pandemic_country

def main():
    print(" Chargement des données dans la base PostgreSQL...")
    
    try:
        load_continent()
        print(" Continent chargé.")
    except Exception as e:
        print(f" Erreur chargement continent: {e}")
    
    try:
        load_country()
        print(" Country chargé.")
    except Exception as e:
        print(f" Erreur chargement country: {e}")
    
    try:
        load_pandemic()
        print(" Pandemic chargé.")
    except Exception as e:
        print(f" Erreur chargement pandemic: {e}")
    
    try:
        load_pandemic_country()
        print(" Pandemic Country chargé.")
    except Exception as e:
        print(f" Erreur chargement pandemic_country: {e}")
    
    try:
        load_daily_pandemic_country()
        print(" Daily Pandemic Country chargé.")
    except Exception as e:
        print(f" Erreur chargement daily_pandemic_country: {e}")

    print(" Chargement terminé.")

if __name__ == "__main__":
    main()
