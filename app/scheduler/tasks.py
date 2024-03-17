from datetime import datetime
from app import db
from app.models.daily_nutrition_menu import DailyNutritionMenu
from . import scheduler

def create_daily_menus():
    users = db.users.find()

    today = datetime.now().date()

    for user in users:
        nutrition_menu = db.nutritionMenus.find_one({'user_id': user._id, 'isDefault': True}) 
        # Check if a menu for today already exists for the user
        existing_menu = DailyNutritionMenu.find_one({'user_id': user._id, 'date': today})
        if existing_menu:
            continue  # Skip if menu already exists for today

        daily_menu = {
            'user_id': user._id,
            'date': today,
            'menu': nutrition_menu['menu']
        }
        db.dailyNutritionMenus.insert_one(daily_menu)

def create_daily_menus_task():
    scheduler.add_job(create_daily_menus, trigger='cron', hour=0, minute=0)