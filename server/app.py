# server/app.py

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS # Import CORS
import os

# Initialize Flask app
app = Flask(__name__)

# Configure SQLAlchemy
# Use an environment variable for the database URI for better practice
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize CORS
# This allows your React frontend (on a different port) to make requests to your Flask API
CORS(app)

# Import your models AFTER db initialization to avoid circular imports
from models import Plant

# --- Routes ---

@app.route('/plants', methods=['GET'])
def get_plants():
    """
    Handles GET requests to /plants.
    Returns a list of all plants.
    """
    plants = Plant.query.all()
    plant_dicts = [plant.to_dict() for plant in plants]
    return jsonify(plant_dicts), 200

@app.route('/plants/<int:id>', methods=['GET'])
def get_plant_by_id(id):
    """
    Handles GET requests to /plants/:id.
    Returns a single plant by its ID.
    """
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({"message": "Plant not found"}), 404
    return jsonify(plant.to_dict()), 200

@app.route('/plants', methods=['POST'])
def create_plant():
    """
    Handles POST requests to /plants.
    Creates a new plant.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    try:
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
            is_in_stock=data.get('is_in_stock', True) # Default to True if not provided
        )
        db.session.add(new_plant)
        db.session.commit()
        return jsonify(new_plant.to_dict()), 201 # 201 Created
    except KeyError as e:
        db.session.rollback()
        return jsonify({"message": f"Missing required field: {e}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error creating plant: {str(e)}"}), 500

@app.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    """
    Handles PATCH requests to /plants/:id.
    Updates an existing plant partially.
    """
    plant = Plant.query.get(id)

    if not plant:
        return jsonify({"message": "Plant not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    try:
        # Update only the fields provided in the request body
        if 'name' in data:
            plant.name = data['name']
        if 'image' in data:
            plant.image = data['image']
        if 'price' in data:
            plant.price = data['price']
        if 'is_in_stock' in data:
            plant.is_in_stock = data['is_in_stock']

        db.session.commit()
        return jsonify(plant.to_dict()), 200 # 200 OK
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating plant: {str(e)}"}), 500

@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    """
    Handles DELETE requests to /plants/:id.
    Deletes a plant by its ID.
    """
    plant = Plant.query.get(id)

    if not plant:
        return jsonify({"message": "Plant not found"}), 404

    try:
        db.session.delete(plant)
        db.session.commit()
        # Return an empty response with 204 No Content for successful deletion
        return make_response('', 204)
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error deleting plant: {str(e)}"}), 500

# --- Error Handling (Optional, but good practice) ---
@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Resource not found"}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"message": "Internal server error"}), 500


if __name__ == '__main__':
    # For development, run on port 5555 as specified
    app.run(port=5555, debug=True)