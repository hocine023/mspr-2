import pandas as pd


df = pd.read_csv("C:/Users/Anes/MSPR/donnes/worldometer_coronavirus_summary_data.csv")

missing_values = df.isnull().sum()
missing_percentage = (missing_values / len(df)) * 100
missing_data = pd.DataFrame({'Valeurs manquantes': missing_values, 'Pourcentage': missing_percentage})
print("Analyse des valeurs manquantes :")
print(missing_data[missing_data["Valeurs manquantes"] > 0].sort_values(by="Pourcentage", ascending=False))

# Détecter les colonnes avec trop de valeurs manquantes (>40%)
cols_high_missing = missing_data[missing_data["Pourcentage"] > 40].index
print("\nColonnes avec plus de 40% de valeurs manquantes :")
print(list(cols_high_missing))

# Détecter les colonnes avec une seule valeur unique
unique_values = df.nunique()
constant_columns = unique_values[unique_values == 1].index
print("\nColonnes constantes (une seule valeur unique) :")
print(list(constant_columns))

#Détection des valeurs illogiques
print("\nDétection des incohérences logiques :")

# Vérifier s'il y a des valeurs négatives dans les colonnes critiques
columns_to_check = ['total_confirmed', 'total_recovered', 'total_deaths', 'active_cases', 'total_tests']
negative_values = df[(df[columns_to_check] < 0).any(axis=1)]
print(f"Nombre de lignes avec des valeurs négatives : {len(negative_values)}")
if not negative_values.empty:
    print(negative_values[columns_to_check])
    
# Vérifier si total_confirmed est supérieur à la population (ce qui est illogique)
if 'population' in df.columns and 'total_confirmed' in df.columns:
    invalid_confirmed = df[df['total_confirmed'] > df['population']]
    print(f"Nombre de lignes où total_confirmed > population : {len(invalid_confirmed)}")
    if not invalid_confirmed.empty:
        print(invalid_confirmed[['population', 'total_confirmed']])


# Vérifier si total_confirmed < total_recovered + total_deaths
if 'total_confirmed' in df.columns and 'total_recovered' in df.columns and 'total_deaths' in df.columns:
    incoherent_cases = df[df['total_confirmed'] < (df['total_recovered'] + df['total_deaths'])]
    print(f"Nombre de lignes incohérentes (total_confirmed < total_recovered + total_deaths) : {len(incoherent_cases)}")

# Vérifier si active_cases est bien calculé
if 'active_cases' in df.columns and 'total_confirmed' in df.columns and 'total_recovered' in df.columns and 'total_deaths' in df.columns:
    incorrect_active_cases = df[df['active_cases'] != (df['total_confirmed'] - (df['total_recovered'] + df['total_deaths']))]
    print(f"Nombre de lignes incohérentes (active_cases mal calculé) : {len(incorrect_active_cases)}")

# Vérifier si serious_or_critical > active_cases (ce qui est impossible)
if 'serious_or_critical' in df.columns and 'active_cases' in df.columns:
    serious_issue = df[df['serious_or_critical'] > df['active_cases']]
    print(f"Nombre de lignes incohérentes (serious_or_critical > active_cases) : {len(serious_issue)}")
# Vérifier si total_tests est bien ≥ total_confirmed
tests_incohérents = df[df['total_tests'] < df['total_confirmed']]
print(f"Nombre de lignes avec total_tests < total_confirmed : {len(tests_incohérents)}")

# Vérifier si total_deaths est bien ≤ total_confirmed
deaths_incohérents = df[df['total_deaths'] > df['total_confirmed']]
print(f"Nombre de lignes avec total_deaths > total_confirmed : {len(deaths_incohérents)}")
print(df[df['total_tests'] < df['total_confirmed']][['total_tests', 'total_confirmed']])

# Vérifier si total_tests < total_confirmed (ce qui est illogique)
if 'total_tests' in df.columns and 'total_confirmed' in df.columns:
    test_issue = df[df['total_tests'] < df['total_confirmed']]
    print(f"Nombre de lignes incohérentes (total_tests < total_confirmed) : {len(test_issue)}")

anomalies = df[df['total_confirmed'] > df['population']]
print("Anomalies détectées :", anomalies[['country', 'total_confirmed', 'population']])
print("Médiane total_recovered :", df['total_recovered'].median())
print("Médiane total_deaths :", df['total_deaths'].median())
print("Médiane total_confirmed :", df['total_confirmed'].median())

print("\nAnalyse terminée.")
