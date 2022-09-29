from code_names_bot_corpus_creator.download.caches import WikiRedirectsCategoriesCache
from code_names_bot_corpus_creator.download.api_downloader import download
from config import WIKI_FILTERED_1
import json
import requests
from urllib.parse import urlencode

GET_URL = (
    lambda params: f"https://en.wikipedia.org/w/api.php?{urlencode(params)}"
)


def make_request(page_title, continue_params=None):
    params = {
        "titles": page_title,
        "prop": "redirects|categories",
        "format": "json"
    }

    if continue_params is not None:
        params = params.update(continue_params)

    r = requests.get(
        url = GET_URL(params),
        headers = {
            "User-Agent": "CodeNamesBot/0.0 (nalu.zou@gmail.com) python-requests/0.0"
        }
    )

    return r


def validate_response(page_title, response):
    if response.status_code != 200:
        print("Invalid status code", page_title, response.text)
        return False

    if list(response.json()["query"]["pages"].keys())[0] == "-1":
        print("Missing page", page_title, response.text)
        return False
    
    return True


def make_request(page_title):
    response = make_request(page_title)

    if not validate_response(response):
        return None
    
    responses = [response.json()]

    while "continue" in response.json():
        response = make_request(page_title, response["continue"])

        if not validate_response(response):
            return None
        
        responses.append(response.json())
    
    return responses


def process_result(key, result):
    return result, result is not None


def main():
    with open(WIKI_FILTERED_1, "r") as file:
        page_id_titles = file.read().splitlines()
        page_id_titles = map(
            lambda page_id_title: page_id_title.split("\t"), page_id_titles
        )
        page_titles = list(map(lambda page_id_title: page_id_title[1], page_id_titles))

    download(
        keys=page_titles,
        make_request=make_request,
        cache=WikiRedirectsCategoriesCache(),
        process_result=process_result,
        chunk_size=20,
        download_rate=50,
    )


if __name__ == "__main__":
    main()
