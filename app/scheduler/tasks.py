from datetime import datetime
from app import db
import logging

def create_daily_menus():
    users = db.users.find()

    today = datetime.now().date().isoformat()

    for user in users:
        nutrition_menu = db.nutritionMenus.find_one({'user_id': user['_id']}) 
        # Check if a menu for today already exists for the user
        if nutrition_menu:
            existing_menu = db.dailyNutritionMenus.find_one({'user_id': user['_id'], 'createdAt': today})
            if existing_menu:
                logging.info("menu already existtttss")
                continue  # Skip if menu already exists for today

            daily_menu = {
                'user_id': user['_id'],
                'date': today,
                'menu': nutrition_menu['menu'],
                'proteinsEaten': 0,
                'caloriesEaten': 0,
                'createdAt': today
            }
            db.dailyNutritionMenus.insert_one(daily_menu)
        else:
            logging.info(f"No nutrition menu")

# def create_daily_menus_task():
    # scheduler.add_job(create_daily_menus, trigger='cron', hour=0, minute=0)