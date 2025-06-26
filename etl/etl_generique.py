import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import os
from etl.etl_coronavirus_summary import process_summary
from etl.etl_coronavirus_daily import process_daily
from etl.etl_monkeypox import process_monkeypox

CLEAN_FOLDER = '../donnes_clean/'

def detect_and_process(file_path):
    filename = os.path.basename(file_path)
    print("Nom du fichier détecté :", filename)

    output_path = os.path.join(CLEAN_FOLDER, f"{filename.replace('.csv', '_clean.csv')}")

    if "worldometer_coronavirus_summary" in filename:
        print("Fichier détecté : Données cumulées (summary)")
        process_summary(file_path,output_path)

        

    elif "worldometer_coronavirus_daily" in filename:
        print("Fichier détecté : Données journalières (daily)")
        process_daily(file_path,output_path)

    elif "monkeypox" in filename:
        print("Fichier détecté : Monkeypox")
        process_monkeypox(file_path,output_path)

    else:
        print("Type de fichier inconnu : aucun traitement associé.")

if __name__ == "__main__":
    file_path = input("Entrez le chemin du fichier à traiter : ")
    detect_and_process(file_path)
