# verify_clean_data.py

import pandas as pd

# Chargement du fichier nettoyé
file_path = "C:/Users/Anes/MSPR/donnes_clean/worldometer_coronavirus_daily_data_clean.csv"
df = pd.read_csv(file_path)

print("\n📊 Vérification du fichier nettoyé :", file_path)

# --- 1. Valeurs manquantes ---
missing = df.isnull().sum()
missing_total = missing[missing > 0]

if missing_total.empty:
    print("✅ Aucune valeur manquante détectée.")
else:
    print("❌ Valeurs manquantes détectées :")
    print(missing_total)

# --- 2. Valeurs négatives ---
columns_to_check = ['daily_new_cases', 'daily_new_deaths', 'active_cases']
negatives = df[(df[columns_to_check] < 0).any(axis=1)]

if negatives.empty:
    print("✅ Aucune valeur négative dans daily_new_cases, daily_new_deaths ou active_cases.")
else:
    print(f"❌ {len(negatives)} lignes contiennent des valeurs négatives.")
    print(negatives[columns_to_check].head())

# --- 3. Incohérences logiques sur les colonnes cumulatives ---
if "cumulative_total_deaths" in df.columns and "cumulative_total_cases" in df.columns:
    incoh_deaths = df[df['cumulative_total_deaths'] > df['cumulative_total_cases']]
    if incoh_deaths.empty:
        print("✅ Aucun cas où cumulative_total_deaths > cumulative_total_cases.")
    else:
        print(f"❌ {len(incoh_deaths)} lignes où cumulative_total_deaths > cumulative_total_cases.")

if "active_cases" in df.columns and "cumulative_total_cases" in df.columns:
    incoh_active = df[df['active_cases'] > df['cumulative_total_cases']]
    if incoh_active.empty:
        print("✅ Aucun cas où active_cases > cumulative_total_cases.")
    else:
        print(f"❌ {len(incoh_active)} lignes où active_cases > cumulative_total_cases.")

# --- 4. Statistiques (médianes utiles) ---
print("\n📌 Médianes :")
for col in ['cumulative_total_cases', 'cumulative_total_deaths', 'active_cases']:
    if col in df.columns:
        print(f"- {col} : {df[col].median()}")

# --- 5. Détection des incohérences logiques ---
print("\n🧪 Détection de lignes incohérentes...")

incoherences = []

# Règle 1 : new cases > active cases
mask1 = df['daily_new_cases'] > df['active_cases']
incoherences.append(df[mask1].assign(issue="daily_new_cases > active_cases"))

# Règle 2 : new deaths > new cases
mask2 = df['daily_new_deaths'] > df['daily_new_cases']
incoherences.append(df[mask2].assign(issue="daily_new_deaths > daily_new_cases"))

# Règle 3 : new cases > 0 alors que active cases == 0
mask3 = (df['daily_new_cases'] > 0) & (df['active_cases'] == 0)
incoherences.append(df[mask3].assign(issue="daily_new_cases > 0 alors que active_cases == 0"))

# Règle 4 : doublons date/pays
duplicates = df.duplicated(subset=['date', 'country'], keep=False)
incoherences.append(df[duplicates].assign(issue="Doublon date/pays"))

# Récapitulatif
incoherent_rows = pd.concat(incoherences).drop_duplicates()

if incoherent_rows.empty:
    print("✅ Aucune incohérence logique détectée.")
else:
    print(f"❌ {len(incoherent_rows)} lignes incohérentes détectées.")
    print(incoherent_rows[['date', 'country', 'issue']].head())

print("\n✅ Vérification terminée.")
