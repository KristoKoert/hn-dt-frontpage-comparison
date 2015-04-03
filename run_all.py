import collection
import aggregation
import analysis
import visualization
from datetime import datetime, timedelta
from time import sleep


def run_every_hour(end):
    run()
    while datetime.now() < end:
        sleep(60)
    run_every_hour(datetime.now()+timedelta(hours=1))


def run():
    print("Running @", datetime.now())
    collection.run()
    aggregation.run()
    analysis.run()
    visualization.run()

run_every_hour(datetime.now())
