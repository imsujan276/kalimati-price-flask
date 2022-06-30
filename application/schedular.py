
from . import utility

def runSaveToDBSchedular(scheduler):
    scheduler.add_job(func=utility.saveToDBCronJob, args=[], trigger='interval', id='saveToDB', seconds=60)
    scheduler.start()
    