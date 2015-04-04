import matplotlib.pyplot as plt
from util import DT_KEY, HN_KEY
import json


def _get_analysis_results():
    return json.load(open("data/analysis_results.json", 'r'))


def _get_nr_of_runs():
    return len(_get_analysis_results()["link_overlap"]["on_runs"]) - 1


def plot_link_overlap():
    overlap_on_runs = _get_analysis_results()["link_overlap"]["on_runs"]
    plt.plot(overlap_on_runs)
    plt.ylabel("Number of overlapping posts")
    plt.xlabel("Run number")
    plt.ylim([0, 30 + 1])
    plt.xlim([1, _get_nr_of_runs()])
    title = "Overlap of links on HackerNews and DataTau frontpages"
    plt.title(title)
    # plt.show()
    plt.savefig('data/plots/link_overlap.png', bbox_inches='tight')
    plt.close()


def plot_new_posts():
    new_posts_dt = _get_analysis_results()["new_posts"][DT_KEY]
    new_posts_hn = _get_analysis_results()["new_posts"][HN_KEY]
    plt.plot(new_posts_hn)
    plt.plot(new_posts_dt)
    plt.legend(["HackerNews", "DataTau"], loc="best")
    plt.ylabel("Number of new posts")
    plt.xlabel("Run number")
    plt.ylim([0, 30 + 1])
    plt.xlim([2, _get_nr_of_runs() - 1])
    title = "Number of new posts on frontpage since last run"
    plt.title(title)
    # plt.show()
    plt.savefig('data/plots/new_posts.png', bbox_inches='tight')
    plt.close()


def _plot_trivia(data_key):
    data_hn = _get_analysis_results()[data_key]["on_runs"][HN_KEY]
    data_dt = _get_analysis_results()[data_key]["on_runs"][DT_KEY]
    plt.plot(data_hn)
    plt.plot(data_dt)
    plt.legend(["HackerNews", "DataTau"], loc="best")
    if data_key == "nr_of_comments":
        ylabel = "Average number of comments"
        xlabel = "Run number"
        ylim_max = max(data_dt + data_hn)
        ylim_buff = ylim_max / 100 * 10
        ylim = [1, ylim_max + ylim_buff]
        xlim = [1, _get_nr_of_runs()]
        title = "Average number of comments on frontpage"
        path = "data/plots/nr_of_comments.png"
    elif data_key == "post_ages":
        ylabel = "Average post age (hours)"
        xlabel = "Run number"
        ylim_max = max(data_dt + data_hn)
        ylim_buff = ylim_max / 100 * 10
        ylim = [0, ylim_max + ylim_buff]
        xlim = [1, _get_nr_of_runs()]
        title = "Average age of post on frontpage"
        path = "data/plots/post_ages.png"
    elif data_key == "scores":
        ylabel = "Average score of post"
        xlabel = "Run number"
        ylim_max = max(data_dt + data_hn)
        ylim_buff = ylim_max / 100 * 10
        ylim = [0, ylim_max + ylim_buff]
        xlim = [1, _get_nr_of_runs()]
        title = "Average score on frontpage"
        path = "data/plots/scores.png"
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.ylim(ylim)
    plt.xlim(xlim)
    title = title
    plt.title(title)
    # plt.show()
    plt.savefig(path, bbox_inches='tight')
    plt.close()


def plot_nr_of_comments():
    _plot_trivia("nr_of_comments")


def plot_post_ages():
    _plot_trivia("post_ages")


def plot_scores():
    _plot_trivia("scores")


def run():
    plot_nr_of_comments()
    plot_post_ages()
    plot_scores()
    plot_link_overlap()
    plot_new_posts()
