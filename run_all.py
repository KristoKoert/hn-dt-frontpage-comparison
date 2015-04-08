import collection
import aggregation
import analysis
import visualization
from datetime import datetime, timedelta
from time import sleep


def run_in_interval(interval_hours):
    next_run_time = datetime.now()
    while True:
        if datetime.now() > next_run_time:
            next_run_time = datetime.now() + timedelta(hours=interval_hours)
            run()
            print("Next run @", next_run_time)
        else:
            sleep(10)


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


run_in_interval(3)
