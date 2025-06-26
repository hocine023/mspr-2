import pandas as pd
import sys
import os
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from sklearn.metrics import mean_squared_error, mean_absolute_error
from models.config_db import connect_to_db
import joblib
os.makedirs("IA/models_ia", exist_ok=True)


def predict_daily_cases_from_db(id_country: int, id_pandemic: int):
    conn = connect_to_db()
    query = """
        SELECT date, daily_new_cases, active_cases
        FROM daily_pandemic_country
        WHERE id_country = %s AND id_pandemic = %s
        ORDER BY date
    """
    df = pd.read_sql(query, conn, params=(id_country, id_pandemic))
    conn.close()

    if df.empty:
        raise ValueError(f"Aucune donnée trouvée pour le pays ID {id_country} et la pandémie ID {id_pandemic}.")

    df['date'] = pd.to_datetime(df['date'])

    df['incidence_7d'] = df['daily_new_cases'].rolling(window=7).sum()
    df['prevalence_7d'] = df['active_cases'].rolling(window=7).mean()
    df['transmission_rate'] = (df['incidence_7d'] / df['prevalence_7d']) * 100
    df['transmission_rate'] = df['transmission_rate'].replace([np.inf, -np.inf], 0).fillna(0)

    for i in range(1, 7 + 1):
        df[f'lag_{i}'] = df['daily_new_cases'].shift(i)

    df.dropna(inplace=True)

    X = df[[f'lag_{i}' for i in range(1, 8)] + ['transmission_rate']]
    y = df['daily_new_cases']

    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)
    model_path = f"IA/models_ia/model_cases_{id_country}_{id_pandemic}.pkl"
    if os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        joblib.dump(model, model_path)

    # prédiction future sur 7 jours
    lags = df['daily_new_cases'].iloc[-7:].tolist()
    transmission_rate = df['transmission_rate'].iloc[-1]
    last_date = df['date'].iloc[-1]

    predictions = []
    for i in range(1, 8):
        future_input = pd.DataFrame(
            [lags + [transmission_rate]],
            columns=[f'lag_{i}' for i in range(1, 8)] + ['transmission_rate']
        )
        y_next = model.predict(future_input)[0]
        predictions.append({
            "day": f"Jour +{i}",
            "date": (last_date + pd.Timedelta(days=i)).strftime("%Y-%m-%d"),
            "predicted_cases": int(y_next)
        })
        lags = lags[1:] + [y_next]

    return predictions


def predict_daily_deaths_from_db(id_country: int, id_pandemic: int):
    conn = connect_to_db()
    query = """
        SELECT date, daily_new_deaths, active_cases
        FROM daily_pandemic_country
        WHERE id_country = %s AND id_pandemic = %s
        ORDER BY date
    """
    df = pd.read_sql(query, conn, params=(id_country, id_pandemic))
    conn.close()

    if df.empty:
        raise ValueError(f"Aucune donnée trouvée pour le pays ID {id_country} et la pandémie ID {id_pandemic}.")

    df['date'] = pd.to_datetime(df['date'])

    df['mortality_rate_7d'] = df['daily_new_deaths'].rolling(window=7).sum() / df['active_cases'].rolling(window=7).mean() * 100
    df['mortality_rate_7d'] = df['mortality_rate_7d'].replace([np.inf, -np.inf], 0).fillna(0)

    for i in range(1, 8):
        df[f'lag_{i}'] = df['daily_new_deaths'].shift(i)

    df.dropna(inplace=True)

    X = df[[f'lag_{i}' for i in range(1, 8)] + ['mortality_rate_7d']]
    y = df['daily_new_deaths']

    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)
    model_path = f"IA/models_ia/model_deaths_{id_country}_{id_pandemic}.pkl"
    if os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        model = CatBoostRegressor(iterations=100, learning_rate=0.1, depth=6, verbose=0)
        model.fit(X_train, y_train)
        joblib.dump(model, model_path)

    # prédiction future sur 7 jours
    lags = df['daily_new_deaths'].iloc[-7:].tolist()
    mortality_rate = df['mortality_rate_7d'].iloc[-1]
    last_date = df['date'].iloc[-1]

    predictions = []
    for i in range(1, 8):
        future_input = pd.DataFrame(
            [lags + [mortality_rate]],
            columns=[f'lag_{i}' for i in range(1, 8)] + ['mortality_rate_7d']
        )
        y_next = model.predict(future_input)[0]
        predictions.append({
            "day": f"Jour +{i}",
            "date": (last_date + pd.Timedelta(days=i)).strftime("%Y-%m-%d"),
            "predicted_deaths": int(y_next)
        })
        lags = lags[1:] + [y_next]

    return predictions

def predict_active_cases_from_db(id_country: int, id_pandemic: int):
    conn = connect_to_db()
    query = """
        SELECT date, active_cases
        FROM daily_pandemic_country
        WHERE id_country = %s AND id_pandemic = %s
        ORDER BY date
    """
    df = pd.read_sql(query, conn, params=(id_country, id_pandemic))
    conn.close()

    if df.empty:
        raise ValueError("Aucune donnée pour les cas actifs.")

    df['date'] = pd.to_datetime(df['date'])

    for i in range(1, 8):
        df[f'lag_{i}'] = df['active_cases'].shift(i)

    df.dropna(inplace=True)
    X = df[[f'lag_{i}' for i in range(1, 8)]]
    y = df['active_cases']
    model_path = f"IA/models_ia/model_active_{id_country}_{id_pandemic}.pkl"
    if os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        joblib.dump(model, model_path)

    lags = df['active_cases'].iloc[-7:].tolist()[::-1]
    last_date = df['date'].iloc[-1]

    predictions = []
    for i in range(1, 8):
        future_input = pd.DataFrame([lags], columns=[f'lag_{j}' for j in range(1, 8)])
        y_next = model.predict(future_input)[0]
        predictions.append({
            "day": f"Jour +{i}",
            "date": (last_date + pd.Timedelta(days=i)).strftime("%Y-%m-%d"),
            "predicted_active_cases": int(y_next)
        })
        lags = lags[1:] + [y_next]

    return predictions
def predict_transmission_rate_from_predictions(cases_predictions, active_cases_predictions):
    # Extraire les valeurs numériques
    total_predicted_cases = sum(p["predicted_cases"] for p in cases_predictions)
    median_active_cases = np.mean([p["predicted_active_cases"] for p in active_cases_predictions])

    # Calcul du taux de transmission
    if median_active_cases == 0:
        return 0.0
    transmission_rate = (total_predicted_cases / median_active_cases) * 100
    return round(transmission_rate, 2)

def detect_risk_of_next_wave_from_predictions(id_pandemic: int):


    conn = connect_to_db()
    countries_query = "SELECT id_country, country FROM country"
    countries = pd.read_sql(countries_query, conn)
    conn.close()

    results = []

    for _, row in countries.iterrows():
        id_country = row["id_country"]
        name = row["country"]
        try:
            cases_pred = predict_daily_cases_from_db(id_country, id_pandemic)
            actives_pred = predict_active_cases_from_db(id_country, id_pandemic)
            tx = predict_transmission_rate_from_predictions(cases_pred, actives_pred)

            risk = "faible"
            if tx > 10:
                risk = "modéré"
            if tx > 20:
                risk = "élevé"

            results.append({
                "country_id": id_country,
                "country_name": name,
                "transmission_rate": tx,
                "risk_level": risk
            })
        except Exception as e:
            print(f"Erreur pour {name}: {e}")
            continue

    return sorted(results, key=lambda x: x["transmission_rate"], reverse=True)


