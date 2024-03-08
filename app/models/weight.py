from app import db
from bson.objectid import ObjectId
import pymongo
import logging

class Weight:
    def __init__(self, user_id, weight, createdAt, imgUrl):
        self.user_id = user_id
        self.weight = weight
        self.createdAt = createdAt
        self.imgUrl = imgUrl

    def save(self):
        weight = {
            "user_id": self.user_id,
            "weight": self.weight,
            "createdAt": self.createdAt,
            "imgUrl": self.imgUrl
        }

        db.weights.insert_one(weight)

    @staticmethod
    def find_by_user_id(user_id):
        weights = db.weights.find({"user_id": user_id}).sort([("createdAt", pymongo.DESCENDING)])
        weights_list = [weight for weight in weights]
        for weight in weights_list:
            weight['_id'] = str(weight['_id'])
        return weights_list
    
    def update(weight_id, updated_weight):
        result = db.weights.update_one({"_id": ObjectId(weight_id)}, {"$set": updated_weight})
        if result.modified_count == 1:
            return True  
        else:
            return False

    def delete(weight_id):
        db.weights.delete_one({"_id": weight_id})

    @staticmethod
    def get_weight_by_createdAt(created_at, user_id):
        weight = db.weights.find_one({"createdAt": created_at, "user_id": user_id})
        if weight:
            weight['_id'] = str(weight['_id'])
        return weight

    
