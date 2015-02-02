import matplotlib.pyplot as plt
import json

ANALYSIS_RESULTS = json.load(open("data/analysis_results.json", 'r'))


def plot_link_overlap():
    overlap_on_runs = ANALYSIS_RESULTS["link_overlap"]["on_runs"]
    plt.plot(overlap_on_runs)
    plt.ylabel("Ylabel")
    plt.xlabel("Xlabel")
    # plt.ylim()
    # plt.xlim()
    plt.title("Title")
    plt.show()


def plot_new_posts():
    pass


def plot_nr_of_comments():
    pass


def plot_post_ages():
    pass
