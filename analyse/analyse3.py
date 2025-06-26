import pandas as pd

# Chargement du fichier
df = pd.read_csv("C:/Users/Anes/MSPR/donnes/worldometer_coronavirus_daily_data.csv")

# --- Analyse des valeurs manquantes ---
missing_values = df.isnull().sum()
missing_percentage = (missing_values / len(df)) * 100
missing_data = pd.DataFrame({'Valeurs manquantes': missing_values, 'Pourcentage': missing_percentage})

print("Analyse des valeurs manquantes :")
print(missing_data[missing_data["Valeurs manquantes"] > 0].sort_values(by="Pourcentage", ascending=False))

# Colonnes avec plus de 40 % de valeurs manquantes
cols_high_missing = missing_data[missing_data["Pourcentage"] > 40].index
print("\nColonnes avec plus de 40% de valeurs manquantes :")
print(list(cols_high_missing))

# Colonnes constantes
unique_values = df.nunique()
constant_columns = unique_values[unique_values == 1].index
print("\nColonnes constantes (une seule valeur unique) :")
print(list(constant_columns))

# --- Détection des incohérences logiques ---
print("\nDétection des incohérences logiques :")

columns_to_check = ['cumulative_total_cases', 'daily_new_cases', 'active_cases', 'cumulative_total_deaths', 'daily_new_deaths']
negative_values = df[(df[columns_to_check] < 0).any(axis=1)]
print(f"Lignes avec des valeurs négatives : {len(negative_values)}")
if not negative_values.empty:
    print(negative_values[columns_to_check])

# Vérifier si cumulative_total_deaths > cumulative_total_cases
deaths_exceed_cases = df[df['cumulative_total_deaths'] > df['cumulative_total_cases']]
print(f"Lignes où cumulative_total_deaths > cumulative_total_cases : {len(deaths_exceed_cases)}")

# Vérifier si active_cases > cumulative_total_cases
active_exceed_cases = df[df['active_cases'] > df['cumulative_total_cases']]
print(f"Lignes où active_cases > cumulative_total_cases : {len(active_exceed_cases)}")

# Médianes pour information
print("\nStatistiques (médianes) :")
print("Médiane cumulative_total_cases :", df['cumulative_total_cases'].median())
print("Médiane cumulative_total_deaths :", df['cumulative_total_deaths'].median())
print("Médiane active_cases :", df['active_cases'].median())

print("\nAnalyse terminée.")
