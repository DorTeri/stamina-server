from flask import Blueprint, request, jsonify
from app.models.daily_nutrition_menu import DailyNutritionMenu
from app import db
from ..middleware.token_decode import verify_firebase_token

daily_nutrition_menu_bp = Blueprint('daily_nutrition_menu_bp', __name__)

@daily_nutrition_menu_bp.route("/daily_nutrition_menus", methods=["GET"])
@verify_firebase_token
def get_nutrition_menus(user_id):
    daily_nutrition_menu = DailyNutritionMenu.find_by_user_id(user_id)
    if daily_nutrition_menu:
        return jsonify(daily_nutrition_menu), 200
    else:
        return jsonify({"error": "daily nutrition menu not found"}), 404

@daily_nutrition_menu_bp.route("/daily_nutrition_menus", methods=["POST"])
def create_nutrition_menu():
    data = request.json
    nutrition_menu = DailyNutritionMenu(**data)
    nutrition_menu.save()
    return jsonify(nutrition_menu.__dict__), 201

@daily_nutrition_menu_bp.route("/daily_nutrition_menus/<nutrition_id>", methods=["PUT"])
def update_nutrition_menu(nutrition_id):
    data = request.json
    if DailyNutritionMenu.update_by_nutrition_id(nutrition_id, data):
        return jsonify({"message": "Nutrition menu updated successfully"}), 200
    else:
        return jsonify({"error": "Nutrition menu not found"}), 404

@daily_nutrition_menu_bp.route("/daily_nutrition_menus/<nutrition_id>", methods=["DELETE"])
def delete_nutrition_menu(nutrition_id):
    if DailyNutritionMenu.delete(nutrition_id):
        return jsonify({"message": "Nutrition menu deleted successfully"}), 200
    else:
        return jsonify({"error": "Nutrition menu not found"}), 404
