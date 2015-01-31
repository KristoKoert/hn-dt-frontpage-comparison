#!/usr/bin/python3

from index import get_index
from bs4 import BeautifulSoup
from util import write_json

DT_KEY = 'http://www.datatau.com'
HN_KEY = 'http://news.ycombinator.com'


def extract_links(html_soup_titles):
    titles = filter(lambda t: t.a is not None, html_soup_titles)
    # 1 extra stray link on both dt and hn, last link on page
    links = list(map(lambda t: t.a.get("href"), titles))[:-1]
    return links


def extract_titles(html_soup):
    return html_soup.find_all("td", class_="title")


def extract_subtexts(html_soup):
    # Filter is for handling the edge case of YC posted posts.
    # Those subtexts have only the age.
    return list(filter(lambda st: st.span is not None,
                       html_soup.find_all("td", class_="subtext")))


def extract_scores(html_soup_subtexts):
    return list(map(lambda st: int(st.span.contents[0].replace(" points", "")),
                    html_soup_subtexts))


def extract_users(html_soup_subtexts):
    return list(map(lambda st: st.a.contents[0], html_soup_subtexts))


def extract_post_ages(html_soup_subtexts):
    def account_for_units(val, st):
        are_in = lambda v1, v2: True if v1 in st or v2 in st else False
        if are_in("minute", "minutes"):
            return val / 60
        elif are_in("hour", "hours"):
            return val
        elif are_in("day", "days"):
            return val * 24

    get_hours = lambda st: account_for_units(
        int(st.contents[3].split()[0]), st.contents[3])

    return list(map(get_hours, html_soup_subtexts))


def extract_nr_of_comments(html_soup_subtexts):
    def get_comment_nr(a_element):
        content = a_element.find_all("a")[1].contents[0]
        return 0 if content == "discuss" else int(content.split()[0])
    return list(map(get_comment_nr,
                    html_soup_subtexts))


def run():
    results = {}
    index = get_index()
    dates = list(index.keys())
    for date in dates:
        hn_html_soup = BeautifulSoup(open(index[date][HN_KEY], "r"))
        dt_html_soup = BeautifulSoup(open(index[date][DT_KEY], "r"))
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
    write_json(results, "data/results.json")
