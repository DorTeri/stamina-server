from app import db
from bson.objectid import ObjectId

class DailyNutritionMenu:
    def __init__(self, title, user_id, menu, proteinsEaten, caloriesEaten):
        self.title = title
        self.user_id = user_id
        self.menu = menu
        self.proteinsEaten = proteinsEaten
        self.caloriesEaten = caloriesEaten

    def save(self):
        daily_nutrition_menu = {
            "title": self.title,
            "user_id": self.user_id,
            "menu": self.menu,
            "proteinsEaten": self.proteinsEaten,
            "caloriesEaten": self.caloriesEaten
        }

        db.dailyNutritionMenus.insert_one(daily_nutrition_menu)

    @staticmethod
    def find_by_user_id(user_id):
        return list(db.dailyNutritionMenus.find({"user_id": user_id}))

    @staticmethod
    def delete(nutrition_id):
        result = db.dailyNutritionMenus.delete_one({"_id": ObjectId(nutrition_id)})
        if result.deleted_count == 1:
            return True 
        else:
            return False

    @staticmethod
    def update_by_nutrition_id(nutrition_id, new_data):
        result = db.dailyNutritionMenus.update_one({"_id": nutrition_id}, {"$set": new_data})
        if result.modified_count == 1:
            return True  
        else:
            return False