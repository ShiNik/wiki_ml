#user define imports
import src.config as config
import src.util as util

#python imports
import requests

def USE_REQUEST(page_name, section_id, do_debug=False):
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "parse", #"parse","query",
        "page": page_name,
        "prop":  "wikitext", #"wikitext","parsetree", "text"
        "section": section_id,
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    text = DATA["parse"]["wikitext"]["*"]
    redirect_page = False
    if text.startswith('this') and "[[" in text and "]]" in text:
        redirect_page = True

    if do_debug:
        file_name = page_name +".txt"
        full_path = util.get_full_output_path(file_name)
        text_file = open(full_path, "w", encoding="utf-8")
        text_file.write(text)
        text_file.close()
    return text, redirect_page

def USE_REQUEST(page_name, do_debug=False):
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "parse", #"parse","query",
        "page": page_name,
        "prop":  "wikitext", #"wikitext","parsetree", "text"
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    text = DATA["parse"]["wikitext"]["*"]
    redirect_page = False
    if text.startswith('this') and "[[" in text and "]]" in text:
        redirect_page = True

    if do_debug:
        file_name = page_name +".txt"
        full_path = util.get_full_output_path(file_name)
        text_file = open(full_path, "w", encoding="utf-8")
        text_file.write(text)
        text_file.close()
    return text, redirect_page