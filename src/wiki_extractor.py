import requests

path_save_data = "D:\\pywikibot\\scripts\\userscripts\\output\\"
path_save_data ="/home/shima/Documents/src/pywikibot/scripts/userscripts/output/"

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
    if do_debug:
        text_file = open(path_save_data+ page_name +".txt", "w", encoding="utf-8")
        text_file.write(text)
        text_file.close()
    return text

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
    if do_debug:
        text_file = open(path_save_data+ page_name +".txt", "w", encoding="utf-8")
        text_file.write(text)
        text_file.close()
    return text