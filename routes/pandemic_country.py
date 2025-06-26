from flask import Blueprint, jsonify, request
from services.pandemic_country import get_cases_by_continent, get_all_pandemic_country, add_pandemic_country, delete_pandemic_country, update_pandemic_country,get_pandemic_country_by_id
from routes.auth import require_api_key

bp = Blueprint('pandemic_country', __name__, url_prefix='/pandemic_country')

# Route pour récupérer toutes les données de pandémie par pays
@bp.route('', methods=['GET'])
def get_pandemic_countries():
    """
    Récupérer toutes les données de pandémie par pays
    ---
    tags:
      - Pandemic_country
    responses:
      200:
        description: Liste des pays avec leurs données pandémiques
        schema:
          type: array
          items:
            type: object
    """
    pandemic_countries = get_all_pandemic_country()
    return jsonify(pandemic_countries)

@bp.route('/continent', methods=['GET'])
def cases_by_continent():
    """
    Récupérer le nombre total de cas par continent
    ---
    tags:
      - Pandemic_country
    responses:
      200:
        description: Répartition des cas par continent
        schema:
          type: array
          items:
            type: object
            properties:
              continent:
                type: string
              cases:
                type: integer
    """
    continent_cases = get_cases_by_continent()
    return jsonify(continent_cases)

# Route pour récupérer les données de pandémie par pays et id_pandemic
@bp.route('/<int:id_country>/<int:id_pandemic>', methods=['GET'])
def get_pandemic_country_by_id_route(id_country, id_pandemic):
    """
    Récupérer les données pandémiques pour un pays et une pandémie spécifique
    ---
    tags:
      - Pandemic_country
    parameters:
      - name: id_country
        in: path
        type: integer
        required: true
      - name: id_pandemic
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Données trouvées
      404:
        description: Aucune donnée trouvée
    """
    pandemic_country = get_pandemic_country_by_id(id_country, id_pandemic)
    if pandemic_country:
        return jsonify(pandemic_country)
    else:
        return jsonify({"message": "Pandemic data not found for the given country and pandemic ID"}), 404


# Route pour ajouter une entrée pour un pays et une pandémie
@bp.route('', methods=['POST'])
@require_api_key
def add_new_pandemic_country():
    """
    Ajouter des données pandémiques pour un pays
    ---
    tags:
      - Pandemic_country
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
            total_confirmed:
              type: integer
            total_deaths:
              type: integer
            total_recovered:
              type: integer
            active_cases:
              type: integer
            total_tests:
              type: integer
    responses:
      201:
        description: Données ajoutées avec succès
    """
    data = request.get_json()
    id_country = data.get('id_country')
    id_pandemic = data.get('id_pandemic')
    total_confirmed = data.get('total_confirmed')
    total_deaths = data.get('total_deaths')
    total_recovered = data.get('total_recovered')
    active_cases = data.get('active_cases')
    total_tests = data.get('total_tests')


    add_pandemic_country(id_country, id_pandemic, total_confirmed, total_deaths, total_recovered,
                         active_cases, total_tests)
    return jsonify({"message": "Données de pandémie ajoutées avec succès"}), 201

# Route pour supprimer une entrée pour un pays et une pandémie
@bp.route('/<int:id_country>/<int:id_pandemic>', methods=['DELETE'])
@require_api_key
def delete_pandemic_country_route(id_country, id_pandemic):
    """
    Supprimer des données pandémiques pour un pays et une pandémie
    ---
    tags:
      - Pandemic_country
    parameters:
      - name: id_country
        in: path
        type: integer
        required: true
      - name: id_pandemic
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Données supprimées avec succès
    """
    delete_pandemic_country(id_country, id_pandemic)
    return jsonify({"message": "Données de pandémie supprimées avec succès"}), 200

# Route pour mettre à jour une entrée pour un pays et une pandémie
@bp.route('/<int:id_country>/<int:id_pandemic>', methods=['PUT'])
@require_api_key
def update_pandemic_country_route(id_country, id_pandemic):
    """
    Mettre à jour les données pandémiques pour un pays
    ---
    tags:
      - Pandemic_country
    parameters:
      - name: id_country
        in: path
        type: integer
        required: true
      - name: id_pandemic
        in: path
        type: integer
        required: true
      - in: body
        name: data
        required: true
        schema:
          type: object
          properties:
            total_confirmed:
              type: integer
            total_deaths:
              type: integer
            total_recovered:
              type: integer
            active_cases:
              type: integer
            total_tests:
              type: integer
    responses:
      200:
        description: Données mises à jour avec succès
    """
    data = request.get_json()
    total_confirmed = data.get('total_confirmed')
    total_deaths = data.get('total_deaths')
    total_recovered = data.get('total_recovered')
    active_cases = data.get('active_cases')
    total_tests = data.get('total_tests')


    update_pandemic_country(id_country, id_pandemic, total_confirmed, total_deaths, total_recovered,
                            active_cases,total_tests)
    return jsonify({"message": "Données de pandémie mises à jour avec succès"}), 200
