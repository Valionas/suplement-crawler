from tld import get_tld, exceptions
from bs4 import BeautifulSoup
import logging


def transform_url(url):
    res = get_tld(url, as_object=True)
    path_list = [char for char in res.parsed_url.path]
    if len(path_list) == 0:
        final_url = res.parsed_url.scheme + '://' + res.parsed_url.netloc
    elif path_list[-1] == '/':
        final_string = ''.join(path_list[:-1])
        final_url = res.parsed_url.scheme + '://' + res.parsed_url.netloc + final_string
    else:
        final_url = url
    return final_url


def parse_html(html_string, target_element, target_class=''):
    link_dict = {}
    target_attributes = None
    soup = BeautifulSoup(html_string, 'html.parser')
    if target_class != '':
        target_attributes = {'class': target_class}

    link_div = soup.find(target_element, target_attributes)
    if link_div is None:
        return link_dict

    # Passing a list to find_all method
    for element in link_div.find_all('a'):
        try:
            element_text = element.get_text("&nbsp;", strip=True)
            link_dict[element_text] = transform_url(element['href'])
        except KeyError:
            logging.error("Something went wrong with fetching href attribute")
            continue
        except exceptions.TldBadUrl:
            logging.error("Could not transform into a norma url")
            continue
    return link_dict
