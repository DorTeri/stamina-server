from flask import Blueprint, request, jsonify
from app.models.workout_program import WorkoutProgram
from app import db
import logging

workout_program_bp = Blueprint('workout_program_bp', __name__)

@workout_program_bp.route("/workout_programs/<user_id>", methods=["GET"])
def get_workout_programs(user_id):
    workout_program = WorkoutProgram.find_by_user_id(user_id)
    if workout_program:
        return jsonify(workout_program), 200
    else:
        return jsonify({"error": "Workout Programs not found"}), 404

@workout_program_bp.route("/workout_programs", methods=["POST"])
def create_workout_program():
    data = request.json
    workout_program = WorkoutProgram(**data)
    workout_program.save()
    return jsonify(workout_program.__dict__), 201

@workout_program_bp.route("/workout_programs/<workout_id>", methods=["PUT"])
def update_workout_program(workout_id):
    data = request.json
    updated_workout_program = WorkoutProgram.update_by_workout_id(workout_id, data)
    if updated_workout_program:
        return jsonify(updated_workout_program), 200
    else:
        return jsonify({"error": "Workout Program not found"}), 404

@workout_program_bp.route("/workout_programs/<workout_id>", methods=["DELETE"])
def delete_workout_program(workout_id):
    if WorkoutProgram.delete(workout_id):
        return jsonify({"message": "Workout Program deleted successfully"}), 200
    else:
        return jsonify({"error": "Workout Program not found"}), 404
