import pytz
from apscheduler.schedulers.background import BackgroundScheduler


TIME_ZONE_MSK = pytz.timezone('Europe/Moscow')

scheduler = BackgroundScheduler()
scheduler.configure(timezone=TIME_ZONE_MSK)


def set_daily_update():
    from app.updating import DataUpdating
    """update data base every 24h in case new words are added"""
    # scheduler.add_job(TextFiltering().update_all_data, trigger='interval', seconds=14, )
    scheduler.add_job(DataUpdating().initialize_all_data, trigger='cron', hour=4, minute=0)



