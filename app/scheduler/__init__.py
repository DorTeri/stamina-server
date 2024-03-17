from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def init_scheduler():
    scheduler.add_job(create_daily_menus_task, trigger='cron', hour=0, minute=0)
    scheduler.start()

from .tasks import create_daily_menus_task
create_daily_menus_task()
