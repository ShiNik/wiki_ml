# user define imports
# python imports
import requests

import src.util as util
from src.log_manager import LogManager


def make_request(page_name, section_id):
    session = requests.Session()

    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "parse",  # "parse","query",
        "page": page_name,
        "prop": "wikitext",  # "wikitext","parsetree", "text"
        "section": section_id,
        "format": "json"
    }

    result = session.get(url=url, params=params)
    data = result.json()

    text = data["parse"]["wikitext"]["*"]
    redirect_page = False
    if text.startswith('this') and "[[" in text and "]]" in text:
        redirect_page = True

    logger = LogManager.instance()
    if logger.debug_enabled():
        file_name = page_name + ".txt"
        full_path = util.get_full_output_path(file_name)
        text_file = open(full_path, "w", encoding="utf-8")
        text_file.write(text)
        text_file.close()
    return text, redirect_page


def make_request(page_name):
    session = requests.Session()

    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "parse",  # "parse","query",
        "page": page_name,
        "prop": "wikitext",  # "wikitext","parsetree", "text"
        "format": "json"
    }

    result = session.get(url=url, params=params)
    data = result.json()

    text = data["parse"]["wikitext"]["*"]
    redirect_page = False
    if text.startswith('this') and "[[" in text and "]]" in text:
        redirect_page = True

    logger = LogManager.instance()
    if logger.debug_enabled():
        file_name = page_name + ".txt"
        full_path = util.get_full_output_path(file_name)
        text_file = open(full_path, "w", encoding="utf-8")
        text_file.write(text)
        text_file.close()
    return text, redirect_page


def make_request_csv():
    session = requests.Session()

    url = "http://www.worldcitiescultureforum.com/assets/city_data/Number_of_international_tourists_per_year_7112018.csv"

    result = session.get(url=url)
    text = result.text
    logger = LogManager.instance()
    if logger.debug_enabled():
        file_name = "international_tourists" + ".txt"
        full_path = util.get_full_output_path(file_name)
        text_file = open(full_path, "w", encoding="utf-8")
        text_file.write(text)
        text_file.close()
    return text
