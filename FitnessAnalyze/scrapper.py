import logging
import time
import requests


def scrape_url(url, delay=0.1):
    logging.debug('Currently scraping: {}'.format(url))
    time.sleep(delay)
    try:
        req = requests.get(url)
        if req.status_code == "404":
            logging.error('Could not find such link')
            return ''
    except requests.exceptions.ConnectionError:
        logging.error('Connection issues have been found.')
        return ''

    return req.text
