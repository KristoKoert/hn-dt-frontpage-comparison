import json
from functools import reduce
from util import HN_KEY, DT_KEY, average

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


def _vals_on_all_dates(key, hn=True, dt=True):
    """Returns a list of values on all dates.

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

    def diff_on_datetimes(d1, d2, hn_or_dt):
        links_on_both_dates = DATA[d1][hn_or_dt]["links"] + \
            DATA[d2][hn_or_dt]["links"]
        return len(links_on_both_dates) - len(set(links_on_both_dates))

    for dt1, dt2 in datetime_pairs:
        results[HN_KEY].append(diff_on_datetimes(dt1, dt2, HN_KEY))
        results[DT_KEY].append(diff_on_datetimes(dt1, dt2, DT_KEY))

    return results


def hn_new_posts():
    """Return nr of new posts ordered by date"""
    new_posts = nr_of_new_posts(True, False)
    new_posts_list = []
    for date in DATETIMES:
        try:
            new_posts_list.append(new_posts[date])
        except KeyError:
            pass
    return new_posts_list


def dt_new_posts():
    """Return nr of new posts ordered by date"""
    new_posts = nr_of_new_posts(False, True)
    return list((diff[DT_KEY] for diff in list(new_posts.values())))


def average_nr_of_comments_all_time():
    return {
        HN_KEY: average(_vals_on_all_dates("nr_of_comments", dt=False)),
        DT_KEY: average(_vals_on_all_dates("nr_of_comments", hn=False))
    }


def most_comments_all_time():
    return {
        HN_KEY: max(_vals_on_all_dates("nr_of_comments", dt=False)),
        DT_KEY: max(_vals_on_all_dates("nr_of_comments", hn=False))
    }


def average_age_of_post():
    return {
        HN_KEY: average(_vals_on_all_dates("post_ages", dt=False)),
        DT_KEY: average(_vals_on_all_dates("post_ages", hn=False))
    }


def oldest_post():
    return {
        HN_KEY: max(_vals_on_all_dates("post_ages", dt=False)),
        DT_KEY: max(_vals_on_all_dates("post_ages", hn=False))
    }


def average_scores():
    return {
        HN_KEY: average(_vals_on_all_dates("scores", dt=False)),
        DT_KEY: average(_vals_on_all_dates("scores", hn=False))
    }


def highest_score():
    return {
        HN_KEY: max(_vals_on_all_dates("scores", dt=False)),
        DT_KEY: max(_vals_on_all_dates("scores", hn=False))
    }


def overall_link_overlap():
    """Returns the overall post overlap percentage."""
    pass
