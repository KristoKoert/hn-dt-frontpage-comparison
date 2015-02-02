import json
from functools import reduce
from util import HN_KEY, DT_KEY, average
from util import write_json

DATA = json.load(open("data/aggregation_results.json", "r"))
DATETIMES = list(DATA.keys())
DATETIMES.sort()


def _apply_to_datetimes(f):
    """Applies function to all dates that the data contains."""
    for datetime in DATETIMES:
        yield f(datetime)


def _flatten_list_of_lists(lists_on_dates):
    """Returns all elements in lists contained in another list."""
    return list(reduce(lambda ld1, ld2: ld1 + ld2, lists_on_dates))


def _pair_datetimes():
    """Returns list of dates paired by current and next."""
    paired_datetimes = []

    def pair_and_return_later_datetime(d1, d2):
        paired_datetimes.append((d1, d2))
        return d2

    reduce(pair_and_return_later_datetime, DATETIMES)
    return paired_datetimes


def _vals_on_all_datetimes(key, hn=True, dt=True):
    """Returns a list of values on all datetimes.

    :param key: The key to the values of interest
    :param hn: Should the values be returned from the HackerNews data
    :param dt: Should the values be returned from the DataTau data
    :returns: All the specified values in a list
    :rtype: list

    """
    on_dates = lambda hn_or_dt: list(_apply_to_datetimes(
        lambda d: DATA[d][hn_or_dt][key]))
    if hn and dt:
        return _flatten_list_of_lists(on_dates(HN_KEY)) + \
            _flatten_list_of_lists(on_dates(DT_KEY))
    elif hn:
        return _flatten_list_of_lists(on_dates(HN_KEY))
    elif dt:
        return _flatten_list_of_lists(on_dates(DT_KEY))
    else:
        return {}


def _overlap_of_links(l):
    nr_of_links = len(l)
    nr_of_non_overlapping_links = (len(set(l)))
    nr_of_overlapping_links = nr_of_links - nr_of_non_overlapping_links
    return nr_of_overlapping_links


def link_overlap_on_datetimes():
    """Returns overlap data of every run."""
    links_on_datetimes = list(_apply_to_datetimes(lambda d:
                                                  DATA[d][DT_KEY]["links"] +
                                                  DATA[d][HN_KEY]["links"]))

    # Overlap of links on any given run
    overlap_on_datetimes = list(map(lambda ld:
                                    _overlap_of_links(ld), links_on_datetimes))

    return overlap_on_datetimes


def average_link_overlap():
    return average(link_overlap_on_datetimes())


def nr_of_new_posts():
    """Returns nr of new posts on either page compared to last run.

    :returns: Nr of new posts since previous run for all runs
    :rtype: dict

    """
    results = {
        HN_KEY: [],
        DT_KEY: []
    }
    datetime_pairs = _pair_datetimes()

    def diff_on_datetimes(dt1, dt2, hn_or_dt):
        links_first_run = DATA[dt1][hn_or_dt]["links"]
        links_second_run = DATA[dt2][hn_or_dt]["links"]
        new_links = 0
        for link in links_second_run:
            if link not in links_first_run:
                new_links += 1
        return new_links

    for dt1, dt2 in datetime_pairs:
        results[HN_KEY].append(diff_on_datetimes(dt1, dt2, HN_KEY))
        results[DT_KEY].append(diff_on_datetimes(dt1, dt2, DT_KEY))

    return results


def average_of_values(key):
    """Returns the average of some value from all data.

    :param key: The key to the values of interest.
    :returns: The averages of some values for HackerNews and DataTau
    :rtype: dict

    """
    return {
        HN_KEY: average(_vals_on_all_datetimes(key, dt=False)),
        DT_KEY: average(_vals_on_all_datetimes(key, hn=False))
    }


def highest_of_values(key):
    """Returns the maximum of some value from all data.

    :param key: The key to the values of interest.
    :returns: The maximums of some values for HackerNews and DataTau
    :rtype: dict

    """
    return {
        HN_KEY: max(_vals_on_all_datetimes(key, dt=False)),
        DT_KEY: max(_vals_on_all_datetimes(key, hn=False))
    }


def averages_on_datetimes(key):
    """Returns the averages of some values on every datetime

    :param key: The key to the value of interest.
    :returns: A list of averages for both HackerNews and DataTau
    :rtype: dict

    """
    averages = {
        HN_KEY: [],
        DT_KEY: []
    }

    for dt in DATETIMES:
        averages[HN_KEY].append(average(DATA[dt][HN_KEY][key]))
        averages[DT_KEY].append(average(DATA[dt][DT_KEY][key]))

    return averages


def highest_values_on_datetimes(key):
    """Returns the max of some values on every datetime

    :param key: The key to the values of interest
    :returns: A list of maxes for both Hackernews and DataTau
    :rtype: dict

    """
    highest_values = {
        HN_KEY: [],
        DT_KEY: []
    }

    for dt in DATETIMES:
        highest_values[HN_KEY].append(max(DATA[dt][HN_KEY][key]))
        highest_values[DT_KEY].append(max(DATA[dt][DT_KEY][key]))

    return highest_values


def run():
    results = {
        "new_posts": nr_of_new_posts(),
        "link_overlap": {
            "average": average_link_overlap(),
            "on_runs": link_overlap_on_datetimes()
        },
        "nr_of_comments": {
            "average": average_of_values("nr_of_comments"),
            "on_runs": averages_on_datetimes("nr_of_comments"),
            "highest": highest_of_values("nr_of_comments")
        },
        "post_ages": {
            "average": average_of_values("post_ages"),
            "on_runs": averages_on_datetimes("post_ages"),
            "highest": highest_of_values("post_ages")
        },
        "scores": {
            "average": average_of_values("scores"),
            "on_runs": averages_on_datetimes("scores"),
            "highest": highest_of_values("scores")
        }
    }
    write_json(results, "data/analysis_results.json")

run()
