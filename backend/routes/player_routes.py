# routes/player_routes.py
from flask import Blueprint, request, jsonify
from models import Player, Country, Club, Position
from extensions import db
from auth import token_required

player_bp = Blueprint('player_bp', __name__, url_prefix='/api/players')


@player_bp.route('/', methods=['GET'])
@token_required
def get_players(current_user):
    players = Player.query.all()
    return jsonify([{
        'id': p.id_player,
        'first_name': p.first_name,
        'last_name': p.last_name,
        'country_born': p.country_born.name if p.country_born else None,
        'country_nationality': p.country_nationality.name if p.country_nationality else None,
        'current_club': p.current_club.name if p.current_club else None,
        'position': p.position.name if p.position else None,
        'foot': p.foot,
        'height_in_cm': p.height_in_cm,
        'retired': p.retired
    } for p in players])


@player_bp.route('/', methods=['POST'])
@token_required
def add_player(current_user):
    data = request.get_json()
    required_fields = ['first_name', 'last_name', 'birth_date']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'First name, last name, and birth date are required.'}), 400
    
    new_player = Player(
        first_name=data['first_name'],
        last_name=data['last_name'],
        id_country_born=data.get('id_country_born'),
        id_country_nationality=data.get('id_country_nationality'),
        birth_date=data['birth_date'],
        id_current_club=data.get('id_current_club'),
        id_position=data.get('id_position'),
        sub_position=data.get('sub_position'),
        foot=data.get('foot'),
        height_in_cm=data.get('height_in_cm'),
        image_url=data.get('image_url'),
        retired=data.get('retired', False)
    )
    
    db.session.add(new_player)
    db.session.commit()
    
    return jsonify({'message': 'Player added successfully.', 'player': {'id': new_player.id_player, 'first_name': new_player.first_name, 'last_name': new_player.last_name}}), 201


@player_bp.route('/<int:id_player>', methods=['GET'])
@token_required
def get_player(current_user, id_player):
    player = Player.query.get_or_404(id_player)
    return jsonify({
        'id': player.id_player,
        'first_name': player.first_name,
        'last_name': player.last_name,
        'country_born': player.country_born.name if player.country_born else None,
        'country_nationality': player.country_nationality.name if player.country_nationality else None,
        'current_club': player.current_club.name if player.current_club else None,
        'position': player.position.name if player.position else None,
        'sub_position': player.sub_position,
        'foot': player.foot,
        'height_in_cm': player.height_in_cm,
        'image_url': player.image_url,
        'retired': player.retired
    })


@player_bp.route('/<int:id_player>', methods=['PUT'])
@token_required
def update_player(current_user, id_player):
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided.'}), 400
    player = Player.query.get_or_404(id_player)
    
    player.first_name = data.get('first_name', player.first_name)
    player.last_name = data.get('last_name', player.last_name)
    player.id_country_born = data.get('id_country_born', player.id_country_born)
    player.id_country_nationality = data.get('id_country_nationality', player.id_country_nationality)
    player.birth_date = data.get('birth_date', player.birth_date)
    player.id_current_club = data.get('id_current_club', player.id_current_club)
    player.id_position = data.get('id_position', player.id_position)
    player.sub_position = data.get('sub_position', player.sub_position)
    player.foot = data.get('foot', player.foot)
    player.height_in_cm = data.get('height_in_cm', player.height_in_cm)
    player.image_url = data.get('image_url', player.image_url)
    player.retired = data.get('retired', player.retired)
    
    db.session.commit()
    
    return jsonify({'message': 'Player updated successfully.', 'player': {
        'id': player.id_player,
        'first_name': player.first_name,
        'last_name': player.last_name,
        'country_born': player.country_born.name if player.country_born else None,
        'country_nationality': player.country_nationality.name if player.country_nationality else None,
        'current_club': player.current_club.name if player.current_club else None,
        'position': player.position.name if player.position else None,
        'sub_position': player.sub_position,
        'foot': player.foot,
        'height_in_cm': player.height_in_cm,
        'image_url': player.image_url,
        'retired': player.retired
    }})


@player_bp.route('/<int:id_player>', methods=['DELETE'])
@token_required
def delete_player(current_user, id_player):
    player = Player.query.get_or_404(id_player)
    db.session.delete(player)
    db.session.commit()
    return jsonify({'message': 'Player deleted successfully.'}), 204
