import json
from code_names_bot_dictionary_compiler.download.api_downloader import download
from code_names_bot_dictionary_compiler.download.caches import OxfordDefinitionsCache
from config import OXFORD_FILTERED_1, MISSING_US_LEMMAS, MISSING_LEMMAS
from credentials import OXFORD_APP_ID, OXFORD_APP_KEY

GET_URL = (
    lambda is_us: f"https://od-api.oxforddictionaries.com/api/v2/words/{'en-us' if is_us else 'en-gb'}"
)
CHUNK_SIZE = 5


def get_request_params(lemma, is_us):
    return {
        "url": GET_URL(is_us),
        "headers": {"app_id": OXFORD_APP_ID, "app_key": OXFORD_APP_KEY},
        "params": {"q": lemma},
    }


def process_result(key, result):
    if result.status_code == 404 and "error" in result.json():
        print("Lemma not in US dict", key, result.json())
        with open(MISSING_US_LEMMAS, "a") as file:
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
        lemma_regions = list(
            map(lambda lemma_region: lemma_region.split("|"), lemma_regions)
        )
        lemma_to_region = {
            lemma_region[0]: lemma_region[1] == "us" for lemma_region in lemma_regions
        }
        lemmas = lemma_to_region.keys()

    with open(MISSING_US_LEMMAS, "r") as file:
        missing_us_lemmas = set(file.read().splitlines())
        for lemma in missing_us_lemmas:
            lemma_to_region[lemma] = False

    with open(MISSING_LEMMAS, "r") as file:
        missing_lemmas = set(file.read().splitlines())
        lemmas = list(filter(lambda lemma: lemma not in missing_lemmas, lemmas))

    download(
        keys=lemmas,
        get_request_params=lambda lemma: get_request_params(
            lemma, lemma_to_region[lemma]
        ),
        cache=OxfordDefinitionsCache(),
        process_result=process_result,
        chunk_size=5,
        download_rate=1,  # Oxford API limits usage to 1 request / second
    )


if __name__ == "__main__":
    main()
