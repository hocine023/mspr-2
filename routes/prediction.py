from flask import Blueprint, jsonify
from IA.predict import predict_daily_cases_from_db, predict_daily_deaths_from_db,predict_active_cases_from_db,predict_transmission_rate_from_predictions,detect_risk_of_next_wave_from_predictions
from services.country import get_all_countries_by_continent,get_all_countries

bp = Blueprint('prediction', __name__)

# Route pour les prédictions de cas
@bp.route('/predict/cases/<int:id_country>/<int:id_pandemic>', methods=['GET'])
def get_cases_prediction(id_country, id_pandemic):
    try:
        predictions = predict_daily_cases_from_db(id_country, id_pandemic)
        return jsonify(predictions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour les prédictions de décès
@bp.route('/predict/deaths/<int:id_country>/<int:id_pandemic>', methods=['GET'])
def get_deaths_prediction(id_country, id_pandemic):
    try:
        predictions = predict_daily_deaths_from_db(id_country, id_pandemic)
        return jsonify(predictions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# Prédiction des cas actifs
@bp.route('/predict/active_cases/<int:id_country>/<int:id_pandemic>', methods=['GET'])
def get_active_cases_prediction(id_country, id_pandemic):
    try:
        predictions = predict_active_cases_from_db(id_country, id_pandemic)
        return jsonify(predictions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Prédiction du taux de transmission moyen basé sur les prédictions
@bp.route('/predict/transmission_rate/<int:id_country>/<int:id_pandemic>', methods=['GET'])
def get_transmission_rate_prediction(id_country, id_pandemic):
    try:
        cases = predict_daily_cases_from_db(id_country, id_pandemic)
        active = predict_active_cases_from_db(id_country, id_pandemic)
        rate = predict_transmission_rate_from_predictions(cases, active)
        return jsonify({"transmission_rate_predicted_7d": rate})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@bp.route('/predict/transmission_rate/continent/<int:id_continent>/<int:id_pandemic>', methods=['GET'])
def get_transmission_rate_by_continent(id_continent, id_pandemic):
   
    countries = get_all_countries_by_continent(id_continent)
    total_pred_cases = []
    total_pred_actives = []

    for country in countries:
        id_country = country[0]
        try:
            cases_pred = predict_daily_cases_from_db(id_country, id_pandemic)
            actives_pred = predict_active_cases_from_db(id_country, id_pandemic)
            total_pred_cases.extend([p['predicted_cases'] for p in cases_pred])
            total_pred_actives.extend([p['predicted_active_cases'] for p in actives_pred])
        except Exception:
            continue  # ignore les erreurs individuelles

    if not total_pred_cases or not total_pred_actives:
        return jsonify({"error": "Données insuffisantes"}), 400

    tx = predict_transmission_rate_from_predictions(
        [{"predicted_cases": v} for v in total_pred_cases],
        [{"predicted_active_cases": v} for v in total_pred_actives]
    )
    return jsonify({
        "id_continent": id_continent,
        "transmission_rate": tx
    })



@bp.route("/predict/next_wave_risk/<int:id_pandemic>", methods=["GET"])
def next_wave_risk(id_pandemic):
    try:
       
        results = detect_risk_of_next_wave_from_predictions(id_pandemic)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

