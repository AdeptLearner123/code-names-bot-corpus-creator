from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
from config import OXFORD_WORD_LIST_DIR
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


GET_URL = lambda page_id: f"https://www.oxfordreference.com/view/10.1093/acref/9780199571123.001.0001/acref-9780199571123?btog=chap&hide=true&pageSize=20&skipEditions=true&sort=titlesort&source=%2F10.1093%2Facref%2F9780199571123.001.0001%2Facref-9780199571123&page={page_id}"
TOTAL_PAGES = 5356


def download(target_pages):
    start_time = time.time()

    with tqdm(total=len(target_pages)) as pbar:
        with ThreadPoolExecutor(max_workers=len(target_pages)) as ex:
            futures = [ex.submit(save_words_from_page, page_id) for page_id in target_pages]
            for future in as_completed(futures):
                pbar.update(1)
    
    print("--- %s seconds ---" % (time.time() - start_time))


def save_words_from_page(page_id):
    output = []
    r = requests.get(GET_URL(page_id), headers={'User-Agent': 'Mozilla/6.0'})
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.select('.itemTitle')
    for item in items:
        word = item.a.find(text=True, recursive=False)
        output.append(word.strip())
    
    with open(os.path.join(OXFORD_WORD_LIST_DIR, f"{page_id}.txt"), "w+") as file:
        file.write("\n".join(output))


def main():
    scraped_pages = os.listdir(OXFORD_WORD_LIST_DIR)
    scraped_pages = set(map(lambda file_name: int(file_name.split(".")[0]), scraped_pages))
    target_pages = range(1, TOTAL_PAGES + 1)
    target_pages = list(filter(lambda page_id: page_id not in scraped_pages, target_pages))

    print("Target pages", len(target_pages))

    download(target_pages)


if __name__ == "__main__":
    main()
