import matplotlib.pyplot as plt
import analyze_data
import pprint
from util import HN_KEY, DT_KEY


def visualize_new_posts():
    data = analyze_data.nr_of_new_posts()
    date_intervals = []
    hn_data = []
    dt_data = []

    for date_interval in list(data.keys()):
        date_intervals.append(str(date_interval))
        hn_data.append(data[date_interval][HN_KEY])
        dt_data.append(data[date_interval][DT_KEY])

    date_intervals.sort()
    plt.plot(hn_data)
    plt.plot(dt_data)
    plt.ylabel("number of new posts")
    plt.xlabel("dates")
    plt.ylim([0, 30])
    plt.xticks(range(len(date_intervals)), date_intervals)
    plt.legend(["HackerNews", "DataTau"], loc="lower right")
    plt.title("New post on HackerNews and DataTau front page across 7 days")
    plt.show()


def visualize_overlap_on_single_days():
    """Incomplete"""
    data = analyze_data.link_overlap()[1]
    sites = analyze_data.DATES
    percentages = list((x * 100 for x in data))
    plt.barh(range(len(percentages)), percentages, align="center")
    plt.yticks(range(len(sites)), sites)
    plt.xlabel("overlap percentage")
    plt.ylabel("dates")
    plt.title("Overlap on single days")
    plt.show()


def run():
    print("Overlap percentage: ", analyze_data.link_overlap()[0])
    pp = pprint.PrettyPrinter(indent=4)
    print("Number of new posts: ")
    pp.pprint(analyze_data.nr_of_new_posts())
    print("Average number of comments: \n",
          analyze_data.average_nr_of_comments())
    print("Most comments: \n", analyze_data.most_comments())
    print("Average age of posts: \n", analyze_data.average_age_of_post())
    print("Oldest post: \n", analyze_data.oldest_post())
    print("Average score: \n", analyze_data.average_scores())
    print("Highest scores: \n", analyze_data.highest_score())

run()
