
from . import utility

def runSaveToDBSchedular(scheduler):
    # cron job per hour * 3
    scheduler.add_job(func=utility.saveToDBCronJob, args=[], trigger='interval', id='saveToDB', seconds=3600*3)
    scheduler.start()
    