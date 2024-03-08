from flask import Blueprint, request, jsonify
from app.models.weight import Weight
from app import db
import logging

weight_bp = Blueprint('weight_bp', __name__)

@weight_bp.route("/weights/<user_id>", methods=["GET"])
def get_weights_by_user_id(user_id):
    weights = Weight.find_by_user_id(user_id)
    if weights:
        return jsonify(weights), 200
    else:
        return jsonify({"error": "weights not found"}), 404

@weight_bp.route("/weights", methods=["POST"])
def create_weight():
    data = request.json
    weight = Weight(**data)
    weight.save()
    return jsonify(weight.__dict__), 201

@weight_bp.route("/weights/<weight_id>", methods=["PUT"])
def update_weight(weight_id):
    data = request.json
    updated_weight = Weight.update(weight_id, data)
    if updated_weight:
        return jsonify(updated_weight), 200
    else:
        return jsonify({"error": "weight not found"}), 404

@weight_bp.route("/weights/<weight_id>", methods=["DELETE"])
def delete_weight(weight_id):
    if Weight.delete(weight_id):
        return jsonify({"message": "Weight deleted successfully"}), 200
    else:
        return jsonify({"error": "Weight not found"}), 404

@weight_bp.route("/weights/created/<user_id>/<created_at>", methods=["GET"])
def get_weight_by_createdAt(user_id, created_at):
    weight = Weight.get_weight_by_createdAt(created_at, user_id)
    if weight:
        return jsonify(weight), 200
    else:
        return jsonify({"error": "Weight not found"}), 404