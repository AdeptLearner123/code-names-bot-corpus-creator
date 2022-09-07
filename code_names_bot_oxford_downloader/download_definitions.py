import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from tqdm import tqdm

from config import FILTERED_WORDLIST_PATH, US_BUT_ACTUALLY_GB
from .oxford_definitions import OxfordDefinitions
from credentials import OXFORD_APP_ID, OXFORD_APP_KEY

GET_URL = lambda is_us: f"https://od-api.oxforddictionaries.com/api/v2/words/{'en-us' if is_us else 'en-gb'}"
CHUNK_SIZE = 5

oxford_definitions = OxfordDefinitions()


def download(terms, term_to_region, us_but_actually_gb):
    start_time = time.time()
    us_but_actuall_gb_set = set(us_but_actually_gb)

    with tqdm(total=len(terms)) as pbar:
        for i in range(0, len(terms), CHUNK_SIZE):
            target_chunk = terms[i : i + CHUNK_SIZE]
            results = dict()

            print("Target ids", len(target_chunk))
            with ThreadPoolExecutor(max_workers=len(target_chunk)) as ex:
                futures = [
                    ex.submit(
                        get_words_result,
                        GET_URL(term_to_region[term] and term not in us_but_actuall_gb_set),
                        term,
                        results
                    )
                    for term in target_chunk
                ]
                for future in as_completed(futures):
                    pbar.update(1)

            chunk_failed = 0
            for term in target_chunk:
                if term not in results:
                    print("Term not in results", term)
                    chunk_failed += 1
                    continue

                if results[term].status_code == 404 and "error" in results[term].json():
                    print("Term not in US dict", term, results[term].json())
                    #chunk_failed += 1
                    us_but_actually_gb.append(term)
                    continue

                if results[term].status_code != 200:
                    print("Invalid status code for", term, results[term].status_code, results[term].text)
                    chunk_failed += 1
                    continue
                    
                oxford_definitions.cache_words_result(term, json.dumps(results[term].json()))

            oxford_definitions.commit()
            with open(US_BUT_ACTUALLY_GB, "w+") as file:
                file.write("\n".join(us_but_actually_gb))

            if chunk_failed > 0:
                print("Chunk Failed", chunk_failed)
                break

            time.sleep(CHUNK_SIZE)

    oxford_definitions.commit()
    print("--- %s seconds ---" % (time.time() - start_time))


def get_words_result(url, term, results):
    r = requests.get(
        url, headers={"app_id": OXFORD_APP_ID, "app_key": OXFORD_APP_KEY}, params={"q": term}
    )
    results[term] = r


def main():
    with open(FILTERED_WORDLIST_PATH, "r") as file:
        terms = file.read().splitlines()

    with open(US_BUT_ACTUALLY_GB, "r") as file:
        us_but_actually_gb = file.read().splitlines()

    cached_terms = oxford_definitions.get_all_cached()
    uncached_terms = list(set(terms).difference(set(cached_terms)))

    print("Terms", len(terms))
    print("Uncached terms", len(uncached_terms))

    download(uncached_terms, oxford_definitions.get_term_to_region(), us_but_actually_gb)


if __name__ == "__main__":
    main()