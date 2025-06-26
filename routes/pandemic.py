from flask import Blueprint, jsonify, request
from services.pandemic import get_all_pandemics, add_pandemic, delete_pandemic, update_pandemic
from routes.auth import require_api_key

# Création d'un Blueprint pour les pandémies
bp = Blueprint('pandemic', __name__, url_prefix='/pandemic')

# Route pour récupérer toutes les pandémies
@bp.route('', methods=['GET'])
def get_pandemics():
    """
    Récupérer toutes les pandémies
    ---
    tags:
      - Pandemic
    responses:
      200:
        description: Liste des pandémies
        schema:
          type: array
          items:
            type: object
            properties:
              id_pandemic:
                type: integer
              name:
                type: string
    """
    pandemics = get_all_pandemics()
    return jsonify(pandemics)

# Route pour ajouter une nouvelle pandémie
@bp.route('', methods=['POST'])
@require_api_key
def add_new_pandemic():
    """
    Ajouter une nouvelle pandémie
    ---
    tags:
      - Pandemic
    parameters:
      - in: body
        name: pandemic
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
    responses:
      201:
        description: Pandémie ajoutée avec succès
      400:
        description: Le nom est requis
    """
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'message': 'Le nom de la pandémie est requis.'}), 400

    add_pandemic(name)
    return jsonify({'message': 'Pandémie ajoutée avec succès.'}), 201

# Route pour supprimer une pandémie
@bp.route('/<int:pandemic_id>', methods=['DELETE'])
@require_api_key
def delete_pandemic_route(pandemic_id):
    """
    Supprimer une pandémie
    ---
    tags:
      - Pandemic
    parameters:
      - name: pandemic_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Pandémie supprimée avec succès
    """
    delete_pandemic(pandemic_id)
    return jsonify({'message': 'Pandémie supprimée avec succès.'}), 200

# Route pour mettre à jour une pandémie
@bp.route('/<int:pandemic_id>', methods=['PUT'])
@require_api_key
def update_pandemic_route(pandemic_id):
    """
    Mettre à jour une pandémie
    ---
    tags:
      - Pandemic
    parameters:
      - name: pandemic_id
        in: path
        type: integer
        required: true
      - in: body
        name: pandemic
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
    responses:
      200:
        description: Pandémie mise à jour avec succès
      400:
        description: Le nom est requis
    """
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'message': 'Le nom de la pandémie est requis.'}), 400

    update_pandemic(pandemic_id, name)
    return jsonify({'message': 'Pandémie mise à jour avec succès.'}), 200
