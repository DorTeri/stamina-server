from flask import Blueprint, request, jsonify
from app.models.token import Token
from app import db

token_bp = Blueprint('token_bp', __name__)

@token_bp.route("/tokens/<user_id>", methods=["GET"])
def find_token_by_user_id(user_id):
    token = Token.find_token_by_user_id(user_id)
    if token:
        return jsonify(token), 200
    else:
        return jsonify({"error": "token not found"}), 404

@token_bp.route("/tokens/token/<token>", methods=["GET"])
def find_id_by_token(token):
    user_id = Token.find_id_by_token(token)
    if user_id:
        return jsonify(user_id), 200
    else:
        return jsonify({"error": "User_id not found"}), 404
    
@token_bp.route("/tokens", methods=["POST"])
def create_token_data():
    data = request.json
    token = Token(**data)
    token.save()
    return jsonify(token.__dict__), 201

@token_bp.route("/tokens/<user_id>", methods=["DELETE"])
def delete_by_user_id(user_id):
    if Token.delete_by_user_id(user_id):
        return jsonify({"message": "Token deleted"}), 200
    else:
        return jsonify({"error": "Token not found"}), 404
    
@token_bp.route("/tokens/token/<token>", methods=["DELETE"])
def delete_by_token(token):
    if Token.delete_by_token(token):
        return jsonify({"message": "Token deleted"}), 200
    else:
        return jsonify({"error": "Token not found"}), 404
