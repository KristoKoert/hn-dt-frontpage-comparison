import json
from functools import reduce
from util import HN_KEY, DT_KEY, average

DATA = json.load(open("data/results.json", "r"))
DATES = list(DATA.keys())
DATES.sort()


def _apply_to_dates(f):
    for date in DATES:
        yield f(date)


def _sum_of_lists_on_dates(lists_on_dates):
    return list(reduce(lambda ld1, ld2: ld1 + ld2, lists_on_dates))


def vals_on_all_dates(key, hn=True, dt=True):
    on_dates = lambda hn_or_dt: list(_apply_to_dates(lambda d:
                                                     DATA[d][hn_or_dt][key]))

    result = {}
    if hn and dt:
        return _sum_of_lists_on_dates(on_dates(HN_KEY)) + \
            _sum_of_lists_on_dates(on_dates(DT_KEY))
    elif hn:
        return _sum_of_lists_on_dates(on_dates(HN_KEY))
    elif dt:
        return _sum_of_lists_on_dates(on_dates(DT_KEY))

    return result


def pair_dates():
    paired_dates = []

    def pair_and_return_later_date(d1, d2):
        paired_dates.append((d1, d2))
        return d2

    reduce(pair_and_return_later_date, DATES)
    return paired_dates


def link_overlap():

    overlap_of_links = lambda l: len(set(l)) / len(l)

    # List of HN and DT links on any given date, ordered by date
    links_on_dates = list(_apply_to_dates(lambda d:
                                          DATA[d][DT_KEY]["links"] +
                                          DATA[d][HN_KEY]["links"]))

    all_links = vals_on_all_dates("links", hn=True, dt=True)

    # Does not account for the edge case of multiple instances
    # of the same link on the front page
    overall_link_overlap = overlap_of_links(all_links)

    # Overlap of links on any given date, ordered by date
    overlap_on_single_dates = list(map(lambda ld:
                                       overlap_of_links(ld[0] + ld[1]),
                                       links_on_dates))

    return overall_link_overlap, overlap_on_single_dates


def nr_of_new_posts():
    results = {}

    date_pairs = pair_dates()

    for date1, date2 in date_pairs:
        # Length of non overlapping links
        diff_hn = int(len(set(
            DATA[date1][HN_KEY]["links"] +
            DATA[date2][HN_KEY]["links"])) / 2)
        diff_dt = int(len(set(
            DATA[date1][DT_KEY]["links"] +
            DATA[date2][DT_KEY]["links"])) / 2)

        results[(date1, date2)] = {
            HN_KEY: diff_hn,
            DT_KEY: diff_dt
        }

    return results


def average_nr_of_comments():
    return {
        HN_KEY: average(vals_on_all_dates("nr_of_comments", dt=False)),
        DT_KEY: average(vals_on_all_dates("nr_of_comments", hn=False))
    }


def most_comments():
    return {
        HN_KEY: max(vals_on_all_dates("nr_of_comments", dt=False)),
        DT_KEY: max(vals_on_all_dates("nr_of_comments", hn=False))
    }


def average_age_of_post():
    return {
        HN_KEY: average(vals_on_all_dates("post_ages", dt=False)),
        DT_KEY: average(vals_on_all_dates("post_ages", hn=False))
    }


def oldest_post():
    return {
        HN_KEY: max(vals_on_all_dates("post_ages", dt=False)),
        DT_KEY: max(vals_on_all_dates("post_ages", hn=False))
    }


def average_scores():
    return {
        HN_KEY: average(vals_on_all_dates("scores", dt=False)),
        DT_KEY: average(vals_on_all_dates("scores", hn=False))
    }


def highest_score():
    return {
        HN_KEY: max(vals_on_all_dates("scores", dt=False)),
        DT_KEY: max(vals_on_all_dates("scores", hn=False))
    }
