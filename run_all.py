import collection
import aggregation
import analysis
import visualization
from datetime import datetime, timedelta
from time import sleep


def run_every_hour(end):
    while datetime.now() < end:
        sleep(15)
    run()
    run_every_hour(datetime.now() + timedelta(hours=1))


def run():
    print("Running @", datetime.now())
    print("Downloading data..")
    collection.run()
    print("Aggregating data..")
    aggregation.run()
    print("Analyzing data..")
    analysis.run()
    print("Creating plots..")
    visualization.run()
    print("Done!")
    

run_every_hour(datetime.now())
