import json
from code_names_bot_corpus_creator.download.caches import WikiRedirectsCategoriesCache
from config import WIKI_FILTERED_1, WIKI_FILTERED_2


def is_disambiguation(json):
    for category in json["categories"]:
        if category["title"] == "Category:Disambiguation pages":
            return True
    
    return False


def has_single_word_title(json):
    for redirect in json["redirects"]:
        redirect_title = redirect["title"].split(" (")[0]
        if len(redirect_title.split(" ")) == 1:
            return True
    return False


def get_redirect_titles(json):
    return [redirect["title"] for redirect in json["redirects"]]


def main():
    with open(WIKI_FILTERED_1) as file:
        page_id_titles = file.read().splitlines()
        page_id_titles = list(map(
            lambda page_id_title: page_id_title.split("\t"), page_id_titles
        ))
        title_to_page_id = { page_id_title[1]: page_id_title[0] for page_id_title in page_id_titles}
        titles = [ page_id_title[1] for page_id_title in page_id_titles ]
    
    cache = WikiRedirectsCategoriesCache()
    title_to_json = cache.get_key_to_value()
    for title in title_to_json:
        title_to_json[title] = json.loads(title_to_json[title])

        if "categories" not in title_to_json[title]:
            print("Missing categories", title)

    titles = filter(lambda title: not is_disambiguation(title_to_json[title]), titles)
    titles = filter(lambda title: has_single_word_title(title_to_json[title]), titles)
    title_to_redirects = { title: get_redirect_titles(title) for title in titles}

    with open(WIKI_FILTERED_2, "w+") as file:
        lines = list(map(lambda title: f"{title_to_page_id[title]}\t{title}\t{'|'.join(title_to_redirects[title])}", titles))
        file.write("\n".join(lines))


if __name__ == "__main__":
    main()
