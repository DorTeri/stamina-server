from app import db
from bson.objectid import ObjectId
import logging

class WorkoutProgram:
    def __init__(self, title, user_id, practiceProgram, muscles):
        self.title = title
        self.user_id = user_id
        self.practiceProgram = practiceProgram
        self.muscles = muscles

    def save(self):
        workout_program = {
            "title": self.title,
            "user_id": self.user_id,
            "practiceProgram": self.practiceProgram,
            "muscles": self.muscles,
        }

        db.workoutPrograms.insert_one(workout_program)

    @staticmethod
    def find_by_user_id(user_id):
        workout_program = db.workoutPrograms.find_one({"user_id": user_id})
        workout_program['_id'] = str(workout_program['_id'])
        return workout_program

    @staticmethod
    def delete(workout_id):
        result = db.workoutPrograms.delete_one({"_id": ObjectId(workout_id)})
        if result.deleted_count == 1:
            return True 
        else:
            return False

    @staticmethod
    def update_by_workout_id(workout_id, new_data):
        result = db.workoutPrograms.update_one({"_id": ObjectId(workout_id)}, {"$set": new_data})
        if result.modified_count == 1:
            updated_workout_program = db.workoutPrograms.find_one({"_id": ObjectId(workout_id)})
            updated_workout_program['_id'] = str(updated_workout_program['_id'])
            return updated_workout_program
        else:
            return None
