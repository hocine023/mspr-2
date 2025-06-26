import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import joblib
import os

def train_model(csv_path, country, model_path):
    data = pd.read_csv(csv_path)
    data['date'] = pd.to_datetime(data['date'])

    country_data = data[data['country'] == country].copy()
    country_data.sort_values('date', inplace=True)
    country_data.reset_index(drop=True, inplace=True)

    for i in range(1, 8):
        country_data[f'lag_{i}'] = country_data['daily_new_cases'].shift(i)

    country_data.dropna(inplace=True)

    X = country_data[[f'lag_{i}' for i in range(1, 8)]]
    y = country_data['daily_new_cases']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = XGBRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)

    print(f"Modèle entraîné pour {country}")
    print(f"RMSE : {rmse:.2f} | MAE : {mae:.2f}")

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    print(f"Modèle sauvegardé dans : {model_path}")
