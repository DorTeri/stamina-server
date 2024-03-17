from functools import wraps
from flask import request, jsonify
from firebase_admin import auth

# Decorator function to verify Firebase token
def verify_firebase_token(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Extract Firebase token from request headers
        firebase_token = request.headers.get('Authorization')
        try:
            # Verify Firebase token
            
            decoded_token = auth.verify_id_token(firebase_token)
            kwargs['user_id'] = decoded_token['uid']
            return func(*args, **kwargs)

        except auth.InvalidIdTokenError:
            return jsonify({'message': 'Invalid Firebase token'}), 401
        except Exception as e:
            return jsonify({'message': str(e)}), 500

    return decorated_function
