from app import db
from bson.objectid import ObjectId


class UserData:
    def __init__(self, age, user_id, programType, gender, activityFactor, goal,
                 practiceType, practicesPerWeek, height, weight, tdee, maxProteins, targetProteins, 
                 targetCalories, stats, weights, markedPractices, monthPracticesMarked, imageUrl):
        self._id = user_id
        self.age = age
        self.programType = programType
        self.gender = gender
        self.activityFactor = activityFactor
        self.goal = goal
        self.practiceType = practiceType
        self.practicesPerWeek = practicesPerWeek
        self.height = height
        self.weight = weight
        self.tdee = tdee
        self.maxProteins = maxProteins
        self.targetProteins = targetProteins
        self.targetCalories = targetCalories
        self.stats = stats
        self.weights = weights
        self.markedPractices = markedPractices
        self.monthPracticesMarked = monthPracticesMarked
        self.imageUrl = imageUrl


    def save(self):
        user_data = {
            "_id": self._id,
            "age": self.age,
            "programType": self.programType,
            "gender": self.gender,
            "activityFactor": self.activityFactor,
            "goal": self.goal,
            "practiceType": self.practiceType,
            "practicesPerWeek": self.practicesPerWeek,
            "height": self.height,
            "weight": self.weight,
            "tdee": self.tdee,
            "maxProteins": self.maxProteins,
            "targetProteins": self.targetProteins,
            "targetCalories": self.targetCalories,
            "stats": self.stats,
            "weights": self.weights,
            "markedPractices": self.markedPractices,
            "monthPracticesMarked": self.monthPracticesMarked,
            "imageUrl": self.imageUrl
        }
        result = db.users.insert_one(user_data)
        user_data['_id'] = str(result.inserted_id)  # Convert ObjectId to string
        return user_data

    @staticmethod
    def find_by_user_id(user_id):
        user = db.users.find_one({"_id": user_id})
        if user:
            user['_id'] = str(user['_id'])
        return user
    
    @staticmethod
    def find_by_user_email(email):
        user = db.users.find_one({"email": email})
        if user:
            user['_id'] = str(user['_id'])  # Convert ObjectId to string
        return user
    
    @staticmethod
    def find_by_username(userName):
        user = db.users.find_one({"userName": userName})
        return user
    
    @staticmethod
    def update_user(user_id, update_data):
        result = db.users.update_one({"_id": user_id}, {"$set": update_data})
        if result.modified_count == 1:
            return True  
        else:
            return False 
    
    @staticmethod
    def delete_user(user_id):
        result = db.users.delete_one({"_id": user_id})
        if result.deleted_count == 1:
            return True 
        else:
            return False  