from flask import Flask
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from flask import jsonify

from routes.country_routes import country_bp
from routes.player_routes import player_bp
from helpers.extensions import db
from helpers.auth import token_required

load_dotenv(".env")

app = Flask(__name__)

# Configure Database URI
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

# Import models here, after db is initialized
from models import (
    Country,
    City,
    Club,
    Position,
    Player,
    Competition,
    Match,
    Appearance,
    Transfer,
    PlayerCareer,
)

# Register blueprints
app.register_blueprint(country_bp)
app.register_blueprint(player_bp)

# Print the DATABASE_URL to verify it's being loaded correctly
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")

# Initialize Firebase Admin SDK
service_account_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred)

# Example Protected Route
@app.route("/api/protected", methods=["GET"])
@token_required
def protected_route(current_user):
    return jsonify({"message": f"Hello, {current_user}!"}), 200

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"message": "Bad Request"}), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"message": "Unauthorized"}), 401

@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Resource Not Found"}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"message": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
