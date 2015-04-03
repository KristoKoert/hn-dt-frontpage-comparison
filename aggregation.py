#!/usr/bin/python3

from indexation import get_index
from bs4 import BeautifulSoup
from util import write_json

DT_KEY = 'http://www.datatau.com'
HN_KEY = 'http://news.ycombinator.com'


def extract_titles(frontpage_soup):
    """Return list of all titles on page. These contain post links."""
    all_titles = frontpage_soup.find_all("td", class_="title")
    post_titles = filter(lambda t: t.get("valign") is None, all_titles)
    return list(post_titles)


def extract_subtexts(frontpage_soup):
    """Return list of all subtexts on page. These contain age, poster etc."""
    # Filter is for handling the edge case of YC posted posts
    return list(filter(lambda st: st.span is not None,
                       frontpage_soup.find_all("td", class_="subtext")))


def extract_links(html_soup_titles):
    """Return list of all links in titles."""
    links = list(map(lambda t: t.a.get("href"), html_soup_titles))
    return links[:-1]  # Remove link to next page


def extract_scores(html_soup_subtexts):
    """Returns list of all scores in subtexts."""
    return list(map(lambda st: int(st.span.contents[0].replace(" points", "")),
                    html_soup_subtexts))


def extract_users(html_soup_subtexts):
    """Returns list of usernames of posters in subtexts."""
    return list(map(lambda st: st.a.contents[0], html_soup_subtexts))


def extract_nr_of_comments(html_soup_subtexts):
    """Returns list of number of comments in subtexts."""
    def get_comment_nr(a_element):
        content = a_element.find_all("a")[1].contents[0]
        return 0 if "discuss" in content else int(content.split()[0])
    return list(map(get_comment_nr,
                    html_soup_subtexts))


def extract_post_ages(html_soup_subtexts):
    """Returns post ages in subtexts.

    :param html_soup_subtexts: List of subtexts
    :returns: List of post ages in hours
    :rtype: list

    """
    def account_for_units(val, st):
        are_in = lambda v1, v2: True if v1 in st or v2 in st else False
        if are_in("minute", "minutes"):
            return val / 60
        elif are_in("hour", "hours"):
            return val
        elif are_in("day", "days"):
            return val * 24
        else:
            raise RuntimeError

    # print(html_soup_subtexts)

    get_hours = lambda st: account_for_units(
        int(str(st.contents[5]).split()[2]), str(st.contents[5]))

    for sub_text in html_soup_subtexts:
        print("Sub Text:", sub_text)
        print("Contents:", sub_text.contents)
        for i in range(len(sub_text.contents)):
            print(i, str(sub_text.contents[i]).split())
        print("Hours:   ", get_hours(sub_text))

    #     assert False
    return list(map(get_hours, html_soup_subtexts))


def run():
    results = {}
    index = get_index()
    datetimes = list(index.keys())
    for date in datetimes:
        hn_html_soup = BeautifulSoup(open(index[date][HN_KEY], "r"))
        dt_html_soup = BeautifulSoup(open(index[date][DT_KEY], "r"))
        dt_html_soup.find_all()
        hn_titles = extract_titles(hn_html_soup)
        hn_subtexts = extract_subtexts(hn_html_soup)
        dt_titles = extract_titles(dt_html_soup)
        dt_subtexts = extract_subtexts(dt_html_soup)
        results[date] = {
            "HackerNews": {
                "links": extract_links(hn_titles),
                "scores": extract_scores(hn_subtexts),
                "users": extract_users(hn_subtexts),
                "post_ages": extract_post_ages(hn_subtexts),
                "nr_of_comments": extract_nr_of_comments(hn_subtexts)
            },
            "DataTau": {
                "links": extract_links(dt_titles),
                "scores": extract_scores(dt_subtexts),
                "users": extract_users(dt_subtexts),
                "post_ages": extract_post_ages(dt_subtexts),
                "nr_of_comments": extract_nr_of_comments(dt_subtexts)
            }
        }
    write_json(results, "data/aggregation_results.json")
