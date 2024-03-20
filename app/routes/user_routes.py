from flask import Blueprint, request, jsonify
from app.models.user_data import UserData
from app import db
from app import app
from flask_bcrypt import Bcrypt
import jwt
import datetime
from functools import wraps
import logging
from ..middleware.token_decode import verify_firebase_token
from app.models.workout_program import WorkoutProgram
from app.models.nutrition_menu import NutritionMenu
from app.models.daily_nutrition_menu import DailyNutritionMenu


bcrypt = Bcrypt(app)

user_bp = Blueprint('user_bp', __name__)

@user_bp.route("/users", methods=["GET"])
@verify_firebase_token
def get_user(user_id):
    
    try:
        # Query MongoDB to retrieve user data
        user_data = db.users.find_one({'_id': user_id})

        if user_data:
            # If user exists, return user data
            return jsonify(user_data), 200
        else:
            return jsonify(None), 202

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@user_bp.route("/users/register", methods=["POST"])
@verify_firebase_token
def create_user(user_id):
    userData = request.json.get("userData")   
    userData["user_id"] = user_id 
    user = UserData(**userData)
    savedUser = user.save()
    
    # Saving workout program
    workout_program_data = request.json.get("workoutProgram")
    workout_program_data["user_id"] = user_id
    workout_program = WorkoutProgram(**workout_program_data)
    workout_program.save()
    
    # Saving nutrition menu
    nutrition_menu_data = request.json.get("nutritionMenu")
    nutrition_menu_data["user_id"] = user_id
    nutrition_menu = NutritionMenu(**nutrition_menu_data)
    nutrition_menu.save()
    
    daily_nutrition_menu_data = request.json.get("nutritionMenu")
    daily_nutrition_menu_data["user_id"] = user_id
    daily_nutrition_menu = DailyNutritionMenu(**daily_nutrition_menu_data)
    daily_nutrition_menu.save()

    return jsonify(savedUser), 201

@user_bp.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    updated_user = UserData.update_user(user_id, data)
    if updated_user:
        return jsonify(updated_user), 200
    else:
        return jsonify({"error": "User not found"}), 404
    
@user_bp.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    deleted_user = UserData.delete_user(user_id)
    if deleted_user:
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404    
    
@user_bp.route("/users/login", methods=["POST"])
def login():
    logging.info("Trying to login")
    print("logging in")
    auth = request.get_json()
    if not auth or 'email' not in auth or 'password' not in auth:
        return jsonify({'message': 'Invalid credentials'}), 401
    user = UserData.find_by_user_email(auth['email'])
    if not user or not bcrypt.check_password_hash(user['password'], auth['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(weeks=1)
    token_payload = {'user_id': user['_id'], 'exp': expiration_time}
    token = jwt.encode(token_payload, app.config['SECRET_KEY'])
    return jsonify({'user': user, 'token': token})

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if the 'Authorization' header is present in the request
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]

        if not token:
            logging.info('Token is missing')
            return jsonify({'message': 'Token is missing'}), 401

        try:
            # Decode the token using the secret key
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            # Extract user ID from the decoded token
            user_id = decoded_token['user_id']
            # Dummy user data retrieval (replace this with your actual user data retrieval logic)
            user = UserData.find_by_user_id(user_id)
            # Here we are simply returning dummy_user_data
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            logging.info('Token has expired')
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            logging.info('Invalid token')
            return jsonify({'message': 'Invalid token'}), 401

    return decorated

# Route to retrieve user information
@user_bp.route('/users', methods=['GET'])
@token_required
def get_user_by_token(user_data):
    return jsonify(user_data)

