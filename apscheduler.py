from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

def ahora():
    print(datetime.now())
    
sched = BackgroundScheduler()

sched.add_job(ahora, 'cron', hour=10, minute=22)

sched.start()

while True:
    pass

