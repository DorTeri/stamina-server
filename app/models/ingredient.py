from app import db
from bson.objectid import ObjectId

class Ingredient:
    def __init__(self, name, amount, code, company,
                  measureUnits, category, group, subCategory):
        self.name = name
        self.amount = amount
        self.code = code
        self.measureUnits = measureUnits
        self.category = category
        self.subCategory = subCategory
        self.company = company
        self.group = group
        
        
    def save(self):
        ingredient_data = {
            "name": self.name,
            "amount": self.amount,
            "code": self.code,
            "measureUnits": self.measureUnits,
            "group": self.group,
            "category": self.category,
            "subCategory": self.subCategory
        }
        db.ingredients.insert_one(ingredient_data)

    @staticmethod
    def find_by_id(ingredient_id):
        ingredient =  db.ingredients.find_one({"_id": ObjectId(ingredient_id)})
        if ingredient:
            ingredient['_id'] = str(ingredient['_id'])
        return ingredient
    
    @staticmethod
    def find_by_code(ingredient_code):
        ingredient = db.ingredients.find_one({"code": ingredient_code})
        if ingredient:
            ingredient['_id'] = str(ingredient['_id'])
        return ingredient

    @staticmethod
    def update(ingredient_id, update_data):
        result = db.ingredients.update_one({"_id": ObjectId(ingredient_id)}, {"$set": update_data})
        if result.modified_count == 1:
            updated_ingredient = db.ingredients.find_one({"_id": ObjectId(ingredient_id)})
            updated_ingredient['_id'] = str(updated_ingredient['_id'])
            return updated_ingredient
        else:
            return None

    @staticmethod
    def delete(ingredient_id):
        result = db.ingredients.delete_one({"_id": ObjectId(ingredient_id)})
        return result.deleted_count > 0
    
    @staticmethod
    def find_by_category(ingredient_category):
        ingredients_cursor = db.ingredients.find({'category': ingredient_category})
        ingredients_list = []

        for ingredient in ingredients_cursor:
            ingredient['_id'] = str(ingredient['_id'])
            ingredients_list.append(ingredient)

        return ingredients_list
    
    @staticmethod
    def find_by_sub_category(ingredient_sub_category):
        ingredients_cursor = db.ingredients.find({'subCategory': ingredient_sub_category})
        ingredients_list = []

        for ingredient in ingredients_cursor:
            ingredient['_id'] = str(ingredient['_id'])
            ingredients_list.append(ingredient)

        return ingredients_list