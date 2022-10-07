from code_names_bot_dictionary_compiler.download.caches import WikiSummariesCache
from code_names_bot_dictionary_compiler.download.api_downloader import download
from config import WIKI_FILTERED_1, MISSING_WIKI_SUMMARIES

from urllib.parse import quote_plus

GET_URL = (
    lambda page_title: f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote_plus(page_title)}"
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
        with open(MISSING_WIKI_SUMMARIES, "a") as file:
            file.write(key + "\n")
        return None, True

    if result.status_code != 200:
        print("Invalid status code", key, result.text)
        return None, False

    json = result.json()
    return json["extract"], True


def main():
    with open(WIKI_FILTERED_1, "r") as file:
        page_id_titles = file.read().splitlines()
        page_id_titles = map(
            lambda page_id_title: page_id_title.split("\t"), page_id_titles
        )
        page_titles = list(map(lambda page_id_title: page_id_title[1], page_id_titles))

    with open(MISSING_WIKI_SUMMARIES, "r") as file:
        missing_summaries = set(file.read().splitlines())

    page_titles = list(
        filter(lambda page_title: page_title not in missing_summaries, page_titles)
    )

    download(
        keys=page_titles,
        get_request_params=get_request_params,
        cache=WikiSummariesCache(),
        process_result=process_result,
        chunk_size=20,
        download_rate=50,
    )


if __name__ == "__main__":
    main()
