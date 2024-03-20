from flask import Blueprint, request, jsonify
from app.models.ingredient import Ingredient
from app import db

ingredient_bp = Blueprint('ingredient_bp', __name__)

@ingredient_bp.route("/ingredients", methods=["GET"])
def get_all_ingredients():
    ingredients = db.ingredients.find()
    return jsonify([ingredient for ingredient in ingredients]), 200

@ingredient_bp.route("/ingredientsids", methods=["GET"])
def get_all_ingredients_by_ids():
    ingredients_ids = request.args.getlist("ids[]")
    
    if not ingredients_ids:
        return jsonify({"error": "No exercise IDs provided in the request."}), 400
    
    ingredients = Ingredient.find_by_ids(ingredients_ids)
    ingredients_serializable = [ingredient for ingredient in ingredients]

    return jsonify(ingredients_serializable), 200

@ingredient_bp.route("/ingredients/<ingredient_id>", methods=["GET"])
def get_ingredient(ingredient_id):
    ingredient = Ingredient.find_by_id(ingredient_id)
    if ingredient:
        return jsonify(ingredient), 200
    else:
        return jsonify({"error": "Ingredient not found"}), 404
    
@ingredient_bp.route("/ingredients/code/<ingredient_code>", methods=["GET"])
def get_ingredient_by_code(ingredient_code):
    ingredient = Ingredient.find_by_code(ingredient_code)  # Assuming you have a method like this
    if ingredient:
        return jsonify(ingredient), 200
    else:
        return jsonify({"error": "Ingredient not found"}), 404    

@ingredient_bp.route("/ingredients", methods=["POST"])
def create_ingredient():
    data = request.json
    ingredient = Ingredient(**data)
    ingredient.save()
    return jsonify(ingredient.__dict__), 201

@ingredient_bp.route("/ingredients/<ingredient_id>", methods=["PUT"])
def update_ingredient(ingredient_id):
    data = request.json
    if Ingredient.update(ingredient_id, data):
        return jsonify({"message": "Ingredient updated successfully"}), 200
    else:
        return jsonify({"error": "Ingredient not found"}), 404

@ingredient_bp.route("/ingredients/<ingredient_id>", methods=["DELETE"])
def delete_ingredient(ingredient_id):
    if Ingredient.delete(ingredient_id):
        return jsonify({"message": "Ingredient deleted successfully"}), 200
    else:
        return jsonify({"error": "Ingredient not found"}), 404
    
@ingredient_bp.route("/ingredients/category/<category>", methods=["GET"])
def get_ingredient_by_category(category):
    ingredient = Ingredient.find_by_category(category) 
    if ingredient:
        return jsonify(ingredient), 200
    else:
        return jsonify({"error": "Ingredients not found"}), 404
    
@ingredient_bp.route("/ingredients/subcategory/<sub_category>", methods=["GET"])
def get_ingredient_by_sub_category(sub_category):
    ingredient = Ingredient.find_by_sub_category(sub_category) 
    if ingredient:
        return jsonify(ingredient), 200
    else:
        return jsonify({"error": "Ingredients not found"}), 404
