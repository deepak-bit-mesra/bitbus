import time
import atexit
from models.timetable import TTRecordModel

from apscheduler.schedulers.background import BackgroundScheduler

# TTRecordModel.cronjobResetValues();

def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    TTRecordModel.cronjobResetValues();


scheduler = BackgroundScheduler()
# This will exucute on every Night 12:00:01 AM 
scheduler.add_job(print_date_time,'cron',hour=0,minute=0,second=1)

scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())