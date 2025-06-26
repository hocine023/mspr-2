from flask import Blueprint, jsonify, request, render_template
from services.continent import get_all_continents, add_continent, delete_continent, update_continent
from routes.auth import require_api_key


bp = Blueprint('continent', __name__, url_prefix='/continent')

# Route pour récupérer tous les continents
@bp.route('', methods=['GET'])
def get_continents():
    """
    Récupérer tous les continents
    ---
    tags:
      - Continent
    responses:
      200:
        description: Liste des continents
        schema:
          type: array
          items:
            type: object
            properties:
              id_continent:
                type: integer
              name:
                type: string
    """
    continents = get_all_continents()
    return jsonify(continents)

# Route pour ajouter un continent
@bp.route('', methods=['POST'])
@require_api_key
def add_new_continent():
    """
    Ajouter un nouveau continent
    ---
    tags:
      - Continent
    parameters:
      - in: body
        name: continent
        required: true
        schema:
          type: object
          properties:
            continent:
              type: string
    responses:
      201:
        description: Continent ajouté avec succès
    """
    data = request.get_json()
    continent_name = data.get('continent')
    add_continent(continent_name)
    return jsonify({"message": "Continent ajouté avec succès"}), 201

# Route pour supprimer un continent
@bp.route('/<int:id>', methods=['DELETE'])
@require_api_key
def delete_continent_route(id):
    """
    Supprimer un continent
    ---
    tags:
      - Continent
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID du continent à supprimer
    responses:
      200:
        description: Continent supprimé avec succès
    """
    delete_continent(id)
    return jsonify({"message": "Continent supprimé avec succès"}), 200

# Route pour mettre à jour un continent
@bp.route('/<int:id>', methods=['PUT'])
@require_api_key
def update_continent_route(id):
    """
    Mettre à jour un continent
    ---
    tags:
      - Continent
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID du continent à mettre à jour
      - in: body
        name: continent
        required: true
        schema:
          type: object
          properties:
            continent:
              type: string
    responses:
      200:
        description: Continent mis à jour avec succès
    """
    data = request.get_json()
    continent_name = data.get('continent')
    update_continent(id, continent_name)
    return jsonify({"message": "Continent mis à jour avec succès"}), 200

