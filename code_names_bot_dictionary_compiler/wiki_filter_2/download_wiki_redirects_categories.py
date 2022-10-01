from code_names_bot_dictionary_compiler.download.caches import WikiRedirectsCategoriesCache
from code_names_bot_dictionary_compiler.download.api_downloader import download
from config import WIKI_FILTERED_1, MISSING_REDIRECTS_CATEGORIES
import json
import requests
from urllib.parse import urlencode

GET_URL = lambda params: f"https://en.wikipedia.org/w/api.php?{urlencode(params)}"


def make_request(page_title, continue_params=None):
    params = {
        "action": "query",
        "titles": page_title,
        "prop": "redirects|categories",
        "format": "json",
    }

    if continue_params is not None:
        params.update(continue_params)

    r = requests.get(
        url=GET_URL(params),
        headers={
            "User-Agent": "CodeNamesBot/0.0 (nalu.zou@gmail.com) python-requests/0.0"
        },
    )

    return r


def validate_response(page_title, response):
    if response.status_code != 200:
        print("Invalid status code", page_title, response.text)
        return False

    return True


def fetch_all_responses(page_title):
    response = make_request(page_title)

    if not validate_response(page_title, response):
        return page_title, None

    responses = [response.json()]

    while "continue" in response.json():
        response = make_request(page_title, response.json()["continue"])

        if not validate_response(page_title, response):
            return page_title, None

        responses.append(response.json())

    return page_title, responses


def process_result(key, result):
    if result is None:
        print("Failed", key)
        return None, False

    if list(result[0]["query"]["pages"].keys())[0] == "-1":
        print("Missing page", key)

        with open(MISSING_REDIRECTS_CATEGORIES, "a") as file:
            file.write(key + "\n")

        return None, True

    return json.dumps(result), True


def main():
    with open(WIKI_FILTERED_1, "r") as file:
        page_id_titles = file.read().splitlines()
        page_id_titles = map(
            lambda page_id_title: page_id_title.split("\t"), page_id_titles
        )
        page_titles = list(map(lambda page_id_title: page_id_title[1], page_id_titles))

    with open(MISSING_REDIRECTS_CATEGORIES, "r") as file:
        missing = set(file.read().splitlines())
        page_titles = list(filter(lambda title: title not in missing, page_titles))

    download(
        keys=page_titles,
        make_request=fetch_all_responses,
        cache=WikiRedirectsCategoriesCache(),
        process_result=process_result,
        chunk_size=20,
        download_rate=20,
    )


if __name__ == "__main__":
    main()
