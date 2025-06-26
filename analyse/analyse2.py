import pandas as pd

# Charger les données
df = pd.read_csv("C:/Users/Anes/MSPR/donnes_clean/worldometer_coronavirus_summary_data_clean.csv")

# Filtrer les lignes contenant au moins une valeur manquante
rows_with_missing_values = df[df.isnull().any(axis=1)]

# Afficher les lignes concernées
print("\nLignes contenant des valeurs manquantes :")
print(rows_with_missing_values)

# Enregistrer ces lignes dans un fichier CSV pour analyse
output_file = "C:/Users/Anes/MSPR/lignes_valeurs_manquantes.csv"
rows_with_missing_values.to_csv(output_file, index=False)

print(f"\nLes lignes avec des valeurs manquantes ont été enregistrées dans {output_file}.")
