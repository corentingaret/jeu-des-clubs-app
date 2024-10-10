# routes/country_routes.py
from flask import Blueprint, request, jsonify
from models import Country
from extensions import db
from auth import token_required

country_bp = Blueprint('country_bp', __name__, url_prefix='/api/countries')

@country_bp.route('/', methods=['GET'])
@token_required
def get_countries(current_user):
    countries = Country.query.all()
    print(f"Number of countries retrieved: {len(countries)}")
    for country in countries:
        print(f"Country: {country.name}, ID: {country.id_country}")
    return jsonify([{'id': c.id_country, 'name': c.name, 'flag': c.flag_emoji} for c in countries])


@country_bp.route('/', methods=['POST'])
@token_required
def add_country(current_user):
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'message': 'Name is required.'}), 400
    new_country = Country(name=data['name'], flag_emoji=data.get('flag_emoji'))
    db.session.add(new_country)
    db.session.commit()
    return jsonify({'message': 'Country added successfully.', 'country': {'id': new_country.id_country, 'name': new_country.name, 'flag': new_country.flag_emoji}}), 201


@country_bp.route('/<int:id_country>', methods=['GET'])
@token_required
def get_country(current_user, id_country):
    country = Country.query.get_or_404(id_country)
    return jsonify({'id': country.id_country, 'name': country.name, 'flag': country.flag_emoji})


@country_bp.route('/<int:id_country>', methods=['PUT'])
@token_required
def update_country(current_user, id_country):
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided.'}), 400
    country = Country.query.get_or_404(id_country)
    country.name = data.get('name', country.name)
    country.flag_emoji = data.get('flag_emoji', country.flag_emoji)
    db.session.commit()
    return jsonify({'message': 'Country updated successfully.', 'country': {'id': country.id_country, 'name': country.name, 'flag': country.flag_emoji}})


@country_bp.route('/<int:id_country>', methods=['DELETE'])
@token_required
def delete_country(current_user, id_country):
    country = Country.query.get_or_404(id_country)
    db.session.delete(country)
    db.session.commit()
    return jsonify({'message': 'Country deleted successfully.'}), 204
