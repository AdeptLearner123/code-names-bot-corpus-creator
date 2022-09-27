from code_names_bot_corpus_creator.download.caches import WikiRedirectsCategoriesCache
from code_names_bot_corpus_creator.download.api_downloader import download
from config import FILTERED_WIKI_PAGES
import json

GET_URL = (
    lambda page_title: f"https://en.wikipedia.org/w/api.php?action=query&titles={page_title}&prop=redirects|categories&format=json"
)


def get_request_params(page_title):
    return {
        "url": GET_URL(page_title),
        "headers": {
            "User-Agent": "CodeNamesBot/0.0 (nalu.zou@gmail.com) python-requests/0.0"
        },
    }


def process_result(key, result):
    if result.status_code != 200:
        print("Invalid status code", key, result.text)
        return None, False

    return json.dumps(result.json()), True


def main():
    with open(FILTERED_WIKI_PAGES, "r") as file:
        page_id_titles = file.read().splitlines()
        page_id_titles = map(
            lambda page_id_title: page_id_title.split("\t"), page_id_titles
        )
        page_titles = list(map(lambda page_id_title: page_id_title[1], page_id_titles))

    download(
        keys=page_titles,
        get_request_params=get_request_params,
        cache=WikiRedirectsCategoriesCache(),
        process_result=process_result,
        chunk_size=20,
        download_rate=10,
    )


if __name__ == "__main__":
    main()
