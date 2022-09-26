import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from tqdm import tqdm

from code_names_bot_corpus_creator.caches.oxford_cache import OxfordCache
from config import (
    FILTERED_LEMMAS,
    MISSING_US_LEMMAS,
    SCRAPED_LEMMAS_US_DIR,
    SCRAPED_LEMMAS_WORLD_DIR,
)
from credentials import OXFORD_APP_ID, OXFORD_APP_KEY

GET_URL = (
    lambda is_us: f"https://od-api.oxforddictionaries.com/api/v2/words/{'en-us' if is_us else 'en-gb'}"
)
CHUNK_SIZE = 5

oxford_cache = OxfordCache()


def download(lemmas, lemma_to_region):
    start_time = time.time()

    with tqdm(total=len(lemmas)) as pbar:
        for i in range(0, len(lemmas), CHUNK_SIZE):
            target_chunk = lemmas[i : i + CHUNK_SIZE]
            results = dict()

            print("Target ids", len(target_chunk))
            with ThreadPoolExecutor(max_workers=len(target_chunk)) as ex:
                futures = [
                    ex.submit(
                        get_lemma_entry,
                        GET_URL(lemma_to_region[lemma]),
                        lemma,
                        results,
                    )
                    for lemma in target_chunk
                ]
                for _ in as_completed(futures):
                    pbar.update(1)

            chunk_failed = 0
            missing_us_lemmas = []
            for lemma in target_chunk:
                if lemma not in results:
                    print("Lemma not in results", lemma)
                    chunk_failed += 1
                    continue

                if (
                    results[lemma].status_code == 404
                    and "error" in results[lemma].json()
                ):
                    print("Lemma not in US dict", lemma, results[lemma].json())
                    missing_us_lemmas.append(lemma)
                    continue

                if results[lemma].status_code != 200:
                    print(
                        "Invalid status code for",
                        lemma,
                        results[lemma].status_code,
                        results[lemma].text,
                    )
                    chunk_failed += 1
                    continue

                oxford_cache.cache_words_result(
                    lemma, json.dumps(results[lemma].json())
                )

            oxford_cache.commit()
            with open(MISSING_US_LEMMAS, "a") as file:
                file.write("\n".join(missing_us_lemmas))

            if chunk_failed > 0:
                print("Chunk Failed", chunk_failed)
                break

            time.sleep(CHUNK_SIZE)

    oxford_cache.commit()
    print("--- %s seconds ---" % (time.time() - start_time))


def get_lemma_entry(url, lemma, results):
    r = requests.get(
        url,
        headers={"app_id": OXFORD_APP_ID, "app_key": OXFORD_APP_KEY},
        params={"q": lemma},
    )
    results[lemma] = r


def main():
    with open(FILTERED_LEMMAS, "r") as file:
        lemma_regions = file.read().splitlines()
        lemma_regions = list(map(lambda lemma_region: lemma_region.split("|"), lemma_regions))
        lemma_to_region = { lemma_region[0]: lemma_region[1] == "us" for lemma_region in lemma_regions }
        lemmas = lemma_to_region.keys()

    cached_lemmas = oxford_cache.get_all_cached()
    uncached_lemmas = list(set(lemmas).difference(set(cached_lemmas)))

    print("Lemmas", len(lemmas))
    print("Uncached lemmas", len(uncached_lemmas))

    download(uncached_lemmas, lemma_to_region)


if __name__ == "__main__":
    main()
