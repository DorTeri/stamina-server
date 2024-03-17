from app import db
from bson.objectid import ObjectId

class Token:
    def __init__(self, user_id, token):
        self._id = user_id
        self.token = token
        
        
    def save(self):
        token_data = {
            "_id": self._id,
            "token": self.token,
        }
        db.tokens.insert_one(token_data)

    @staticmethod
    def find_token_by_user_id(user_id):
        token_doc = db.tokens.find_one({"_id": user_id})
        if token_doc:
            return token_doc.get("token") 
        return None
    
    @staticmethod
    def find_id_by_token(token):
        token_doc = db.tokens.find_one({"token": token})
        if token_doc:
            return str(token_doc.get("_id")) 
        return None


    @staticmethod
    def delete_by_user_id(user_id):
        result = db.tokens.delete_one({"_id": user_id})
        return result.deleted_count > 0
    
    @staticmethod
    def delete_by_token(token):
        result = db.tokens.delete_one({"token": token})
        return result.deleted_count > 0
    
    