
from . import utility

def runSaveToDBSchedular(scheduler):
    # hourly cron job
    scheduler.add_job(func=utility.saveToDBCronJob, args=[], trigger='interval', id='saveToDB', seconds=3600)
    scheduler.start()
    