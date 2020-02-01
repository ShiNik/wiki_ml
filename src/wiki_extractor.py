import pywikibot
import requests

path_save_data = "D:\\pywikibot\\scripts\\userscripts\\output\\"
path_save_data ="/home/shima/Documents/src/pywikibot/scripts/userscripts/output/"

def print_sections(sections, level=0):
    for s in sections:
        print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[:]))
        print_sections(s.sections, level + 1)

def print_links(page):
    links = page.links
    for title in sorted(links.keys()):
        print("%s: %s" % (title, links[title]))

def print_categories(page):
    categories = page.categories
    for title in sorted(categories.keys()):
        print("%s: %s" % (title, categories[title]))

def print_categorymembers(categorymembers, level=0, max_level=1):
    for c in categorymembers.values():
        print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            print_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)

def USE_WIKI_API(page_name):
    import wikipediaapi
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page_wiki = wiki_wiki.page(page_name)
    print_categories(page_wiki)

    cat = wiki_wiki.page("Category:Tourism-related lists of superlatives")
    print("Category members: Category:Tourism-related lists of superlatives")
    print_categorymembers(cat.categorymembers)

    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )

    page_wiki = wiki_wiki.page('List of most visited museums')
    print("Page - Exists: %s" % page_wiki.exists())
    print("Page - Title: %s" % page_wiki.title)
    print("Page - Summary: %s" % page_wiki.summary[0:60])
    print(page_wiki.fullurl)
    print(page_wiki.canonicalurl)
    print(page_wiki.text)
    print_sections(page_wiki.sections)

    wiki_html = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.HTML
    )

    page_html = wiki_wiki.page('List of most visited museums')
    print("Page - Exists: %s" % page_html.exists())
    print("Page - Title: %s" % page_html.title)
    print("Page - Summary: %s" % page_html.summary[0:60])
    print(page_html.fullurl)
    print(page_html.canonicalurl)
    print(page_html.text)

def USE_WIKI_BOT(page_name, do_debug=False):
    if "State Hermitage Museum" in page_name:
        print("shima")
    site = pywikibot.Site()
    page = pywikibot.Page(site, page_name)
    redirect_page = page.isRedirectPage()
    text = page.text
    if do_debug:
        text_file = open(path_save_data + page_name + ".txt", "w", encoding="utf-8")
        text_file.write(text)
        text_file.close()
        print(text)
    return text, redirect_page

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