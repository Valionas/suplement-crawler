import logging
import urllib.robotparser

from html_parser import parse_html
from scrapper import scrape_url

def is_fetchable(url, default_delay = 0.5):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url("{}robots.txt".format(url))
    rp.read()
    delay = rp.crawl_delay("*")
    can_fetch = rp.can_fetch("*", url)
    if delay is None:
        delay = default_delay

    return can_fetch, delay

def crawler_consume_url(seed_url, max_n=1):
    delay_time = 1
    target_element = 'body'
    target_class = ''
    initial_url_set = set()
    initial_url_list = []
    seen_url_set = set()
    initial_url_set.add(seed_url)
    initial_url_list.append(seed_url)
    link_dictionaries = []
    while len(initial_url_set) != 0 and len(seen_url_set) < max_n:
        temp_url = initial_url_set.pop()
        if temp_url in seen_url_set:
            continue
        else:
            seen_url_set.add(temp_url)
            can_crawl, delay = is_fetchable(temp_url, delay_time)
            # if not can_crawl:
            #     logging.error("URL {} should not be crawled, skipping".format(temp_url))
            #     continue
            req_text = scrape_url(temp_url, delay)
            links_dictionary = parse_html(req_text, target_element, target_class)
            site_dictionary = {
                "site": temp_url,
                "urls": links_dictionary
            }
            link_dictionaries.append(site_dictionary)
    return link_dictionaries
