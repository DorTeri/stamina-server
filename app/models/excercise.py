from app import db
from bson.objectid import ObjectId
import logging

class Excercise:
    def __init__(self, name, hebrewName, label, mainMuscle, videoName,
                 groupMuscle, exerciseType, isRecommended, isRm1,hebrewDescription,englishDescription, exerciseMethod):
        self.name = name
        self.hebrewName = hebrewName
        self.label = label
        self.mainMuscle = mainMuscle
        self.videoName = videoName
        self.groupMuscle = groupMuscle
        self.exerciseType = exerciseType
        self.isRecommended = isRecommended
        self.isRm1 = isRm1
        self.hebrewDescription = hebrewDescription
        self.englishDescription = englishDescription
        self.exerciseMethod = exerciseMethod
        
    def save(self):
        exercise_data = {
            "name": self.name,
            "hebrewName": self.hebrewName,
            "label": self.label,
            "mainMuscle": self.mainMuscle,
            "videoName": self.videoName,
            "groupMuscle": self.groupMuscle,
            "exerciseType": self.exerciseType,
            "isRecommended": self.isRecommended,
            "isRm1": self.isRm1,
            "hebrewDescription": self.hebrewDescription,
            "englishDescription": self.englishDescription,
            "exerciseMethod": self.exerciseMethod
        }
        db.exercises.insert_one(exercise_data)

    @staticmethod
    def find_by_id(exercise_id):
        exercise = db.exercises.find_one({"_id": ObjectId(exercise_id)})
        if exercise:
            exercise['_id'] = str(exercise['_id'])
        return exercise
    
    @staticmethod
    def find_by_ids(exercise_ids):
        object_ids = [ObjectId(exercise_id) for exercise_id in exercise_ids]

        exercises = list(db.exercises.find({"_id": {"$in": object_ids}}))
    
        for exercise in exercises:
            exercise['_id'] = str(exercise['_id'])
        return exercises
    
    @staticmethod
    def update(exercise_id, update_data):
        result = db.exercises.update_one({"_id": ObjectId(exercise_id)}, {"$set": update_data})
        return result.modified_count > 0

    @staticmethod
    def delete(exercise_id):
        result = db.exercises.delete_one({"_id": ObjectId(exercise_id)})
        return result.deleted_count > 0
    
    @staticmethod
    def find_by_main_muscle(main_muscle):
        exercises_cursor = db.exercises.find({'mainMuscle': main_muscle})
        exercises_list = []

        for exercise in exercises_cursor:
            exercise['_id'] = str(exercise['_id'])
            exercises_list.append(exercise)

        return exercises_list