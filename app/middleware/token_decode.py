from functools import wraps
from flask import request, jsonify
import logging
from firebase_admin import auth

# Decorator function to verify Firebase token
def verify_firebase_token(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Extract Firebase token from request headers
        firebase_token = request.headers.get('Authorization').split(' ')[1]
        logging.info(f"token: {firebase_token}")
        try:
            # Verify Firebase token
            if firebase_token:
                decoded_token = auth.verify_id_token(firebase_token)
                logging.info(f"Decoded token: {decoded_token}")
                kwargs['user_id'] = decoded_token['uid']
                return func(*args, **kwargs)
            else:
                return jsonify({'message': 'Authorization header missing'}), 401

        except auth.InvalidIdTokenError:
            logging.error('Invalid Firebase token')
            return jsonify({'message': 'Invalid Firebase token'}), 401
        except Exception as e:
            logging.error(f'Error verifying Firebase token: {e}')
            return jsonify({'message': 'Error verifying Firebase token'}), 500

    return decorated_function
