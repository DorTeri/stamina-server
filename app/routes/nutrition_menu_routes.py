from flask import Blueprint, request, jsonify
from app.models.nutrition_menu import NutritionMenu
from app.models.daily_nutrition_menu import DailyNutritionMenu
from app import db
from ..middleware.token_decode import verify_firebase_token

nutrition_menu_bp = Blueprint('nutrition_menu_bp', __name__)

@nutrition_menu_bp.route("/nutrition_menus", methods=["GET"])
@verify_firebase_token
def get_nutrition_menus(user_id):
    nutrition_menu = NutritionMenu.find_by_user_id(user_id)
    if nutrition_menu:
        return jsonify(nutrition_menu), 200
    else:
        return jsonify({"error": "Nutrition menus not found"}), 404

@nutrition_menu_bp.route("/nutrition_menus", methods=["POST"])
def create_nutrition_menu():
    data = request.json
    nutrition_menu = NutritionMenu(**data)
    nutrition_menu.save()
    nutrition_menu['proteinsEaten'] = 0
    nutrition_menu['caloriesEaten'] = 0
    DailyNutritionMenu(**data)
    return jsonify(nutrition_menu.__dict__), 201

@nutrition_menu_bp.route("/nutrition_menus/<nutrition_id>", methods=["PUT"])
def update_nutrition_menu(nutrition_id):
    data = request.json
    if NutritionMenu.update_by_nutrition_id(nutrition_id, data):
        return jsonify({"message": "Nutrition menu updated successfully"}), 200
    else:
        return jsonify({"error": "Nutrition menu not found"}), 404

@nutrition_menu_bp.route("/nutrition_menus/<nutrition_id>", methods=["DELETE"])
def delete_nutrition_menu(nutrition_id):
    if NutritionMenu.delete(nutrition_id):
        return jsonify({"message": "Nutrition menu deleted successfully"}), 200
    else:
        return jsonify({"error": "Nutrition menu not found"}), 404
