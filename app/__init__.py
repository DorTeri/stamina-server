from flask import Flask
from pymongo import MongoClient
import logging
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_pyfile('config.py')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


client = MongoClient(app.config['MONGO_URI'])
db = client[app.config['MONGO_DB']]

@app.route("/")
def hello():
    logging.info('testtt')
    return 'Hello world!'
    

from app.routes.user_routes import user_bp
from app.routes.excercise_routes import exercise_bp
from app.routes.ingredient_routes import ingredient_bp
from app.routes.workout_program_routes import workout_program_bp
from app.routes.nutrition_menu_routes import nutrition_menu_bp
from app.routes.daily_nutrition_menu_routes import daily_nutrition_menu_bp
app.register_blueprint(user_bp)
app.register_blueprint(exercise_bp)
app.register_blueprint(ingredient_bp)
app.register_blueprint(workout_program_bp)
app.register_blueprint(nutrition_menu_bp)
app.register_blueprint(daily_nutrition_menu_bp)
