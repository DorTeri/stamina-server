from flask import Flask
from pymongo import MongoClient
import logging
from flask_cors import CORS
from firebase_admin import credentials, initialize_app
# from .config.firebase_config import FIREBASE_ADMIN_SDK_CREDENTIALS
from .config.firebase_config_aws import get_secret
from .config.firebase_config import FIREBASE_ADMIN_SDK_CREDENTIALS

app = Flask(__name__)
CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_pyfile('config.py')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# FIREBASE_ADMIN_SDK_CREDENTIALS = get_secret()
cred = credentials.Certificate(FIREBASE_ADMIN_SDK_CREDENTIALS)
default_app = initialize_app(cred)

client = MongoClient(app.config['MONGO_URI'])
db = client[app.config['MONGO_DB']]
    

from app.routes.user_routes import user_bp
from app.routes.excercise_routes import exercise_bp
from app.routes.ingredient_routes import ingredient_bp
from app.routes.workout_program_routes import workout_program_bp
from app.routes.nutrition_menu_routes import nutrition_menu_bp
from app.routes.daily_nutrition_menu_routes import daily_nutrition_menu_bp
from app.routes.weight_routes import weight_bp
from app.routes.token_routes import token_bp
app.register_blueprint(user_bp)
app.register_blueprint(exercise_bp)
app.register_blueprint(ingredient_bp)
app.register_blueprint(workout_program_bp)
app.register_blueprint(nutrition_menu_bp)
app.register_blueprint(daily_nutrition_menu_bp)
app.register_blueprint(weight_bp)
app.register_blueprint(token_bp)

from apscheduler.schedulers.background import BackgroundScheduler
from .scheduler.tasks import create_daily_menus

scheduler = BackgroundScheduler()

def init_scheduler():
    scheduler.add_job(create_daily_menus, trigger='cron', hour=0 , minute=0)
    scheduler.start()
    
init_scheduler()

