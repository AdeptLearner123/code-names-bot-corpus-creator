from code_names_bot_corpus_creator.download.caches import WikiPageViewCache
from code_names_bot_corpus_creator.download.api_downloader import download
from config import WIKI_FILTERED_2, MISSING_WIKI_PAGE_VIEWS

from urllib.parse import urlencode

GET_URL = (
    lambda page_title: f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{urlencode(page_title)}/monthly/2021010100/2021123100"
)


def get_request_params(page_title):
    return {
        "url": GET_URL(page_title),
        "headers": {
            "User-Agent": "CodeNamesBot/0.0 (nalu.zou@gmail.com) python-requests/0.0"
        },
    }


def process_result(key, result):
    if result.status_code == 404:
        print("Not found", key)
        with open(MISSING_WIKI_PAGE_VIEWS, "a") as file:
            file.write(key + "\n")
        return None, True

    if result.status_code != 200:
        print("Invalid status code", key, result.text)
        return None, False

    json = result.json()
    monthly_views = [item["views"] for item in json["items"]]
    return sum(monthly_views), True


def main():
    with open(WIKI_FILTERED_2, "r") as file:
        page_id_titles = file.read().splitlines()
        page_id_titles = map(
            lambda page_id_title: page_id_title.split("\t"), page_id_titles
        )
        page_titles = list(map(lambda page_id_title: page_id_title[1], page_id_titles))

    with open(MISSING_WIKI_PAGE_VIEWS, "r") as file:
        missing_page_views = set(file.read().splitlines())

    page_titles = list(
        filter(lambda page_title: page_title not in missing_page_views, page_titles)
    )

    download(
        keys=page_titles,
        get_request_params=get_request_params,
        cache=WikiPageViewCache(),
        process_result=process_result,
        chunk_size=20,
        download_rate=1.5,
    )


if __name__ == "__main__":
    main()
