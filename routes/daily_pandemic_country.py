from flask import Blueprint, request, jsonify
from routes.auth import require_api_key
from services.daily_pandemic_country import (
    get_daily_data,
    add_daily_data,
    update_daily_data,
    delete_daily_data,
    get_total_cases_and_deaths,
    get_monkeypox_daily_by_continent
)

bp = Blueprint('daily_pandemic_country', __name__, url_prefix='/daily_pandemic_country')

@bp.route('/<int:id_country>/<int:id_pandemic>', methods=['GET'])
@bp.route('/<int:id_country>/<int:id_pandemic>/<string:date>', methods=['GET'])
def get_daily_data_route(id_country, id_pandemic, date=None):
    """
    Récupérer les données journalières pour un pays et une pandémie
    ---
    tags:
      - Daily Pandemic Country
    parameters:
      - name: id_country
        in: path
        required: true
        type: integer
      - name: id_pandemic
        in: path
        required: true
        type: integer
      - name: date
        in: path
        required: false
        type: string
        format: date
    responses:
      200:
        description: Données journalières récupérées
      404:
        description: Aucune donnée trouvée
      400:
        description: Mauvais format de date
    """
    try:
        if date:  # Si une date est fournie dans l'URL
            daily_data = get_daily_data(id_country, id_pandemic, date)
            if daily_data:
                return jsonify(daily_data)
            else:
                return jsonify({"message": "No daily data found for the given parameters"}), 404
        else:  # Si aucune date n'est fournie
            all_daily_data = get_daily_data(id_country, id_pandemic)
            if all_daily_data:
                return jsonify(all_daily_data)
            else:
                return jsonify({"message": "No daily data found for the given country and pandemic"}), 404
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

@bp.route('/totals/<int:id_country>/<int:id_pandemic>', methods=['GET'])
def get_total_stats_route(id_country, id_pandemic):
    """
    Récupérer la somme des cas et des décès pour un pays et une pandémie
    ---
    tags:
      - Daily Pandemic Country
    parameters:
      - name: id_country
        in: path
        required: true
        type: integer
      - name: id_pandemic
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Totaux des cas et décès retournés avec succès
      500:
        description: Erreur serveur
    """
    try:
        stats = get_total_cases_and_deaths(id_country, id_pandemic)
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
      
      
@bp.route('/monkeypox/continent', methods=['GET'])
def get_monkeypox_continent_route():
    """
    Récupérer les données agrégées par continent pour Monkeypox
    ---
    tags:
      - Daily Pandemic Country
    responses:
      200:
        description: Données agrégées par continent
    """
    data = get_monkeypox_daily_by_continent()
    return jsonify(data), 200



@bp.route('', methods=['POST'])
@require_api_key
def add_daily_pandemic_country():
    """
    Ajouter des données journalières pour un pays et une pandémie
    ---
    tags:
      - Daily_pandemic_country
    parameters:
      - in: body
        name: data
        required: true
        schema:
          type: object
          properties:
            id_country:
              type: integer
            id_pandemic:
              type: integer
            date:
              type: string
              format: date
            daily_new_cases:
              type: integer
            daily_new_deaths:
              type: integer
            active_cases:
              type: integer
    responses:
      201:
        description: Données journalières ajoutées avec succès
    """
    data = request.get_json()
    id_country = data.get('id_country')
    id_pandemic = data.get('id_pandemic')
    date = data.get('date')
    daily_new_cases = data.get('daily_new_cases')
    daily_new_deaths = data.get('daily_new_deaths')
    active_cases = data.get('active_cases')

    add_daily_pandemic_country(id_country, id_pandemic, date, daily_new_cases, daily_new_deaths, active_cases)
    return jsonify({"message": "Données journalières ajoutées avec succès"}), 201


@bp.route('/<int:id_country>/<int:id_pandemic>/<string:date>', methods=['PUT'])
@require_api_key
def update_daily_pandemic_country(id_country, id_pandemic, date):
    """
    Mettre à jour les données journalières pour un pays et une pandémie à une date donnée
    ---
    tags:
      - Daily_pandemic_country
    parameters:
      - name: id_country
        in: path
        required: true
        type: integer
      - name: id_pandemic
        in: path
        required: true
        type: integer
      - name: date
        in: path
        required: true
        type: string
        format: date
      - in: body
        name: data
        required: true
        schema:
          type: object
          properties:
            daily_new_cases:
              type: integer
            daily_new_deaths:
              type: integer
            active_cases:
              type: integer
    responses:
      200:
        description: Données mises à jour avec succès
    """
    data = request.get_json()
    daily_new_cases = data.get('daily_new_cases')
    daily_new_deaths = data.get('daily_new_deaths')
    active_cases = data.get('active_cases')

    update_daily_data(id_country, id_pandemic, date, daily_new_cases, daily_new_deaths, active_cases)
    return jsonify({"message": "Données journalières mises à jour avec succès"}), 200


# Supprimer des données journalières
@bp.route('/<int:id_country>/<int:id_pandemic>/<string:date>', methods=['DELETE'])
@require_api_key
def delete_daily_data_route(id_country, id_pandemic, date):
    """
    Supprimer des données journalières
    ---
    tags:
      - Daily Pandemic Country
    parameters:
      - name: id_country
        in: path
        required: true
        type: integer
      - name: id_pandemic
        in: path
        required: true
        type: integer
      - name: date
        in: path
        required: true
        type: string
        format: date
    responses:
      200:
        description: Données journalières supprimées avec succès
    """
    delete_daily_data(id_country, id_pandemic, date)
    return jsonify({"message": "Daily data deleted successfully"})
