import pandas as pd

# Chargement du fichier
df = pd.read_csv("C:/Users/Anes/MSPR/donnes/owid-monkeypox-data.csv", parse_dates=['date'])

# --- Analyse des valeurs manquantes ---
missing_values = df.isnull().sum()
missing_percentage = (missing_values / len(df)) * 100
missing_data = pd.DataFrame({'Valeurs manquantes': missing_values, 'Pourcentage': missing_percentage})

print("Analyse des valeurs manquantes :")
print(missing_data[missing_data["Valeurs manquantes"] > 0].sort_values(by="Pourcentage", ascending=False))

# ---Colonnes avec plus de 40 % de NaN ---
cols_high_missing = missing_data[missing_data["Pourcentage"] > 40].index
print("\nColonnes avec plus de 40% de valeurs manquantes :")
print(list(cols_high_missing))

# --- Colonnes constantes ---
unique_values = df.nunique()
constant_columns = unique_values[unique_values == 1].index
print("\nColonnes constantes (une seule valeur unique) :")
print(list(constant_columns))

# ---Détection des incohérences logiques ---
print("\nDétection des incohérences logiques :")

# Colonnes numériques principales à contrôler
columns_to_check = ['total_cases', 'total_deaths', 'new_cases', 'new_deaths']
columns_to_check = [col for col in columns_to_check if col in df.columns]

# Valeurs négatives
negative_values = df[(df[columns_to_check] < 0).any(axis=1)]
print(f"Lignes avec des valeurs négatives : {len(negative_values)}")
if not negative_values.empty:
    print(negative_values[columns_to_check])

# Vérifier si total_deaths > total_cases
if 'total_deaths' in df.columns and 'total_cases' in df.columns:
    deaths_exceed_cases = df[df['total_deaths'] > df['total_cases']]
    print(f"Lignes où total_deaths > total_cases : {len(deaths_exceed_cases)}")

# ---Médianes ---
print("\nStatistiques (médianes) :")
for col in ['total_cases', 'total_deaths', 'new_cases', 'new_deaths']:
    if col in df.columns:
        print(f"Médiane {col} :", df[col].median())

print("\nAnalyse terminée.")
