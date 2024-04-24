from app import db
from bson.objectid import ObjectId
import logging

class Ingredient:
    def __init__(self, name, amount, code, company,
                  measureUnits, category, group, subCategory, servingType):
        self.name = name
        self.amount = amount
        self.code = code
        self.measureUnits = measureUnits
        self.category = category
        self.subCategory = subCategory
        self.company = company
        self.group = group
        self.servingType = servingType
        
        
    def save(self):
        ingredient_data = {
            "name": self.name,
            "amount": self.amount,
            "code": self.code,
            "measureUnits": self.measureUnits,
            "group": self.group,
            "company": self.company,
            "category": self.category,
            "subCategory": self.subCategory,
            "servingType": self.servingType
        }
        db.ingredients.insert_one(ingredient_data)

    @staticmethod
    def find_by_id(ingredient_id):
        ingredient =  db.ingredients.find_one({"_id": ObjectId(ingredient_id)})
        if ingredient:
            ingredient['_id'] = str(ingredient['_id'])
        return ingredient
    
    @staticmethod
    def find_by_ids(ingredients_ids):
        object_ids = [ObjectId(ingredient_id) for ingredient_id in ingredients_ids]

        ingredients = list(db.ingredients.find({"_id": {"$in": object_ids}}))
    
        for ingredient in ingredients:
            ingredient['_id'] = str(ingredient['_id'])
        return ingredients
    
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
    def find_by_category(ingredient_category, search_text):
        query = {'category': ingredient_category}
        if search_text:
            query['name'] = {'$regex': search_text, '$options': 'i'}
            
        ingredients_cursor = db.ingredients.find(query)
        ingredients_list = []

        for ingredient in ingredients_cursor:
            ingredient['_id'] = str(ingredient['_id'])
            ingredients_list.append(ingredient)

        return ingredients_list
    
    
    @staticmethod
    def find_by_sub_category(ingredient_sub_category, search_text):
        query = {'category': ingredient_sub_category}
        if search_text:
            query['name'] = {'$regex': search_text, '$options': 'i'}
        ingredients_cursor = db.ingredients.find(query)
        ingredients_list = []

        for ingredient in ingredients_cursor:
            ingredient['_id'] = str(ingredient['_id'])
            ingredients_list.append(ingredient)

        return ingredients_list
    
    @staticmethod
    def find_by_name(search_text):
        ingredients_cursor = db.ingredients.find({'$regex': search_text, '$options': 'i'})
        ingredients_list = []

        for ingredient in ingredients_cursor:
            ingredient['_id'] = str(ingredient['_id'])
            ingredients_list.append(ingredient)

        return ingredients_list
    
    
    @staticmethod
    def get_all_categories():
        categories = db.ingredients.distinct('category')
        return categories
    
    
    @staticmethod
    def get_all_categories():
        categories = db.ingredients.distinct('category')
        return categories
    
    @staticmethod
    def get_sub_categories_by_category(category):
    # Find all documents in the 'ingredients' collection with the specified category
        ingredients_cursor = db.ingredients.find({'category': category})
    # Create a set to store unique sub-categories
        sub_categories_set = set()

    # Iterate over the documents and collect unique sub-categories
        for ingredient in ingredients_cursor:
            sub_category = ingredient.get('subCategory')
            if sub_category:
                sub_categories_set.add(sub_category)

    # Convert the set to a list and return
        sub_categories_list = list(sub_categories_set)
        return sub_categories_list