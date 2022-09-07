import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

CHUNK_SIZE = 100


def scrape(url_maker, target_ids, extractor, save_dir, headers):
    scraped_pages = os.listdir(save_dir)
    scraped_pages = set(
        map(lambda file_name: file_name.split(".txt")[0], scraped_pages)
    )
    unscraped_ids = list(
        filter(lambda target_id: target_id not in scraped_pages, target_ids)
    )

    print("Target pages", len(unscraped_ids))

    download(unscraped_ids, url_maker, extractor, save_dir, headers)


def download(target_ids, url_maker, extractor, save_dir, headers):
    start_time = time.time()

    with tqdm(total=len(target_ids)) as pbar:
        for i in range(0, len(target_ids), CHUNK_SIZE):
            target_chunk = target_ids[i : i + CHUNK_SIZE]
            results = dict()

            print("Target ids", len(target_chunk))
            with ThreadPoolExecutor(max_workers=len(target_ids)) as ex:
                futures = [
                    ex.submit(
                        save_words_from_page,
                        url_maker(page_id),
                        page_id,
                        results,
                        headers,
                    )
                    for page_id in target_chunk
                ]
                for future in as_completed(futures):
                    pbar.update(1)

            chunk_failed = 0
            print("Results", len(results))
            for page_id in target_chunk:
                if page_id not in results:
                    chunk_failed += 1
                    continue

                soup = BeautifulSoup(results[page_id], "html.parser")

                try:
                    output = extractor(soup)
                except:
                    print("Failed for", url_maker(page_id))
                    print(results[page_id])
                    raise

                if len(output) > 0:
                    with open(os.path.join(save_dir, f"{page_id}.txt"), "w+") as file:
                        file.write("\n".join(output))
                else:
                    chunk_failed += 1

            if chunk_failed > 0:
                print("Chunk Failed", chunk_failed)
                break

    print("--- %s seconds ---" % (time.time() - start_time))


def save_words_from_page(url, page_id, results, headers):
    r = requests.get(url, headers=headers)
    results[page_id] = r.text
