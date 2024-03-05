from flask import Blueprint, request, jsonify
from app.models.excercise import Excercise
from app import db
import logging

exercise_bp = Blueprint('exercise_bp', __name__)

@exercise_bp.route("/exercises", methods=["GET"])
def get_all_exercises():
    logging.info("inside exercises")
    exercises = db.exercises.find()
    exercises_list = list(exercises)  
    
    for exercise in exercises_list:
        exercise['_id'] = str(exercise['_id'])
    
    return jsonify(exercises_list), 200

@exercise_bp.route("/exercisesids", methods=["GET"])
def get_exercises_by_ids():
    exercise_ids = request.args.getlist("ids[]")

    if not exercise_ids:
        return jsonify({"error": "No exercise IDs provided in the request."}), 400

    exercises = Excercise.find_by_ids(exercise_ids)

    exercises_serializable = [exercise for exercise in exercises]

    return jsonify(exercises_serializable), 200

@exercise_bp.route("/exercises/<exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = Excercise.find_by_id(exercise_id)
    if exercise:
        return jsonify(exercise), 200
    else:
        return jsonify({"error": "Exercise not found"}), 404

@exercise_bp.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.json
    exercise = Excercise(**data)
    exercise.save()
    return jsonify(exercise.__dict__), 201

@exercise_bp.route("/exercises/<exercise_id>", methods=["PUT"])
def update_exercise(exercise_id):
    data = request.json
    if Excercise.update(exercise_id, data):
        return jsonify({"message": "Exercise updated successfully"}), 200
    else:
        return jsonify({"error": "Exercise not found"}), 404

@exercise_bp.route("/exercises/<exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    if Excercise.delete(exercise_id):
        return jsonify({"message": "Exercise deleted successfully"}), 200
    else:
        return jsonify({"error": "Exercise not found"}), 404

@exercise_bp.route("/exercises/main_muscle/<main_muscle>", methods=["GET"])
def get_exercises_by_main_muscle(main_muscle):

    return Excercise.find_by_main_muscle(main_muscle)
