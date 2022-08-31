from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
from config import OXFORD_WORD_LIST_DIR
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


GET_URL = lambda page_id: f"https://www.oxfordreference.com/view/10.1093/acref/9780199571123.001.0001/acref-9780199571123?btog=chap&hide=true&pageSize=20&skipEditions=true&sort=titlesort&source=%2F10.1093%2Facref%2F9780199571123.001.0001%2Facref-9780199571123&page={page_id}"
TOTAL_PAGES = 5356
CHUNK_SIZE = 100


def download(target_pages):
    start_time = time.time()
    failed = 0

    with tqdm(total=len(target_pages)) as pbar:
        for i in range(0, len(target_pages), CHUNK_SIZE):
            target_chunk = target_pages[i:i + CHUNK_SIZE]
            results = dict()

            with ThreadPoolExecutor(max_workers=len(target_pages)) as ex:   
                futures = [ex.submit(save_words_from_page, page_id, results) for page_id in target_chunk]
                for future in as_completed(futures):
                    pbar.update(1)
            
            chunk_failed = 0
            for page_id in results:
                if len(results[page_id]) > 0:
                    with open(os.path.join(OXFORD_WORD_LIST_DIR, f"{page_id}.txt"), "w+") as file:
                        file.write("\n".join(results[page_id]))
                else:
                    chunk_failed += 1
            failed += chunk_failed
            print("Chunk Failed", chunk_failed)
    
    print("Failed", failed)
    print("--- %s seconds ---" % (time.time() - start_time))


def prune():
    count = 0
    for file_name in tqdm(os.listdir(OXFORD_WORD_LIST_DIR)):
        file_path = os.path.join(OXFORD_WORD_LIST_DIR, file_name)
        with open(file_path, "r") as file:
            if len(file.read().splitlines()) == 0:
                count += 1
                os.remove(file_path)
    print("Pruned", count)


def save_words_from_page(page_id, results):
    output = []
    r = requests.get(GET_URL(page_id), headers={'User-Agent': 'Mozilla/6.0'})
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.select('.itemTitle')
    for item in items:
        word = item.a.find(text=True, recursive=False)
        output.append(word.strip())
    
    results[page_id] = output


def main():
    #prune()
    #return

    scraped_pages = os.listdir(OXFORD_WORD_LIST_DIR)
    scraped_pages = set(map(lambda file_name: int(file_name.split(".")[0]), scraped_pages))
    target_pages = range(1, TOTAL_PAGES + 1)
    target_pages = list(filter(lambda page_id: page_id not in scraped_pages, target_pages))

    print("Target pages", len(target_pages))

    download(target_pages)


if __name__ == "__main__":
    main()
