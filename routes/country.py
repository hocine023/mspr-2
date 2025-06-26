from flask import Blueprint, jsonify, request
from services.country import get_all_countries, add_country, delete_country, update_country,get_country_by_id,get_all_countries_by_continent


bp = Blueprint('country', __name__, url_prefix='/country')

# Route pour récupérer tous les pays
@bp.route('', methods=['GET'])
def get_countries():
    """
    Récupérer tous les pays
    ---
    tags:
      - Country
    responses:
      200:
        description: Liste des pays
        schema:
          type: array
          items:
            type: object
            properties:
              id_country:
                type: integer
              country:
                type: string
              population:
                type: integer
              id_continent:
                type: integer
    """
    countries = get_all_countries()
    return jsonify(countries)
  
@bp.route('/continent/<int:id_continent>', methods=['GET'])
def get_countries_by_continent(id_continent):
    """
    Récupérer les pays par continent
    ---
    parameters:
      - name: id_continent
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Liste des pays du continent
    """
    try:
        countries = get_all_countries_by_continent(id_continent)
        return jsonify(countries)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
  
@bp.route('/<int:id>', methods=['GET'])
def get_country(id):
    """
    Récupérer les détails d'un pays par ID
    ---
    tags:
      - Country
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID du pays
    responses:
      200:
        description: Détails du pays
        schema:
          type: object
          properties:
            id_country:
              type: integer
            country:
              type: string
            population:
              type: integer
            id_continent:
              type: integer
      404:
        description: Pays non trouvé
    """
    country = get_country_by_id(id)
    if country:
        return jsonify(country)
    else:
        return jsonify({"error": "Pays non trouvé"}), 404

# Route pour ajouter un pays
@bp.route('', methods=['POST'])
def add_new_country():
    """
    Ajouter un nouveau pays
    ---
    tags:
      - Country
    parameters:
      - in: body
        name: country
        required: true
        schema:
          type: object
          properties:
            country:
              type: string
            population:
              type: integer
            Id_continent:
              type: integer
    responses:
      201:
        description: Pays ajouté avec succès
    """
    data = request.get_json()
    country_name = data.get('country')
    population = data.get('population')
    id_continent = data.get('Id_continent')
    add_country(country_name, population, id_continent)
    return jsonify({"message": "Pays ajouté avec succès"}), 201

# Route pour supprimer un pays
@bp.route('/<int:id>', methods=['DELETE'])
def delete_country_route(id):
    """
    Supprimer un pays
    ---
    tags:
      - Country
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID du pays à supprimer
    responses:
      200:
        description: Pays supprimé avec succès
    """
    delete_country(id)
    return jsonify({"message": "Pays supprimé avec succès"}), 200

# Route pour mettre à jour un pays
@bp.route('/<int:id>', methods=['PUT'])
def update_country_route(id):
    """
    Mettre à jour un pays
    ---
    tags:
      - Country
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID du pays à mettre à jour
      - in: body
        name: country
        required: true
        schema:
          type: object
          properties:
            country:
              type: string
            population:
              type: integer
            Id_continent:
              type: integer
    responses:
      200:
        description: Pays mis à jour avec succès
    """
    data = request.get_json()
    country_name = data.get('country')
    population = data.get('population')
    id_continent = data.get('Id_continent')
    update_country(id, country_name, population, id_continent)
    return jsonify({"message": "Pays mis à jour avec succès"}), 200
