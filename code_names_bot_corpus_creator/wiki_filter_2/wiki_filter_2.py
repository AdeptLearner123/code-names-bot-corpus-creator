import json
from code_names_bot_corpus_creator.download.caches import WikiRedirectsCategoriesCache
from config import WIKI_FILTERED_1, WIKI_FILTERED_2


def is_disambiguation(results):
    for result in results:
        page_result = list(result["query"]["pages"].values())[0]
        for category in page_result["categories"]:
            if category["title"] == "Category:Disambiguation pages":
                return True
    
    return False


def has_single_word_title(redirects):
    return any(redirect.split(" ") == 1 for redirect in redirects)


def get_redirect_titles(results):
    redirects = []
    for result in results:
        page_result = list(result["query"]["pages"].values())[0]

        if "redirects" not in page_result:
            print("Missing redirects", result)

        if "redirects" in page_result:
            for redirect in page_result["redirects"]:
                redirect_title = redirect["title"].split(" (")[0]
                redirects.append(redirect_title)
    return redirects


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

    title_to_redirects = { title: get_redirect_titles(title_to_json[title]) for title in title_to_json }

    titles = filter(lambda title: title in title_to_json, titles)
    titles = filter(lambda title: not is_disambiguation(title_to_json[title]), titles)
    titles = filter(lambda title: has_single_word_title(title_to_redirects[title]), titles)

    with open(WIKI_FILTERED_2, "w+") as file:
        lines = list(map(lambda title: f"{title_to_page_id[title]}\t{title}\t{'|'.join(title_to_redirects[title])}", titles))
        file.write("\n".join(lines))


if __name__ == "__main__":
    main()
