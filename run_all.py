import collection
import aggregation
import analysis
import visualization
from datetime import datetime, timedelta
from time import sleep


def run_every_six_hours(end):
    run()
    while datetime.now() < end:
        sleep(60)
    run_every_six_hours(datetime.now()+timedelta(hours=6))


def run():
    collection.run()
    aggregation.run()
    analysis.run()
    visualization.run()

run_every_six_hours(datetime.now())
