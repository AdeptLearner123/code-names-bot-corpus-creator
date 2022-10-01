import json
from code_names_bot_dictionary_compiler.download.api_downloader import download
from code_names_bot_dictionary_compiler.download.caches import OxfordSentencesCache
from config import OXFORD_FILTERED_1, MISSING_SENTENCES
from credentials import OXFORD_APP_ID, OXFORD_APP_KEY

GET_URL = (
    lambda lemma: f"https://od-api.oxforddictionaries.com/api/v2/sentences/en/{lemma}?strictMatch=false"
)
CHUNK_SIZE = 5


def get_request_params(lemma):
    return {
        "url": GET_URL(lemma),
        "headers": {
            "Accept": "application/json",
            "app_id": OXFORD_APP_ID,
            "app_key": OXFORD_APP_KEY,
        },
    }


def process_result(key, result):
    if result.status_code == 404:
        print("Missing", key)
        with open(MISSING_SENTENCES, "a") as file:
            file.write(key + "\n")
        return None, True

    if result.status_code != 200:
        print(
            "Invalid status code for",
            key,
            result.status_code,
            result.text,
        )
        return None, False

    return json.dumps(result.json()), True


def main():
    with open(OXFORD_FILTERED_1, "r") as file:
        lemma_regions = file.read().splitlines()
        lemmas = list(
            map(lambda lemma_region: lemma_region.split("|")[0], lemma_regions)
        )

    with open(MISSING_SENTENCES, "r") as file:
        missing_sentences = set(file.read().splitlines())
        lemmas = list(filter(lambda lemma: lemma not in missing_sentences, lemmas))

    download(
        keys=lemmas,
        get_request_params=get_request_params,
        cache=OxfordSentencesCache(),
        process_result=process_result,
        chunk_size=5,
        download_rate=1,  # Oxford API limits usage to 1 request / second
    )


if __name__ == "__main__":
    main()
