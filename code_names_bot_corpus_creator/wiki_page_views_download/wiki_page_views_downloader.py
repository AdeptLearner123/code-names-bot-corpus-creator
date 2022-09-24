import os
import subprocess
import sys
import time
from tqdm import tqdm
from config import WIKI_PAGE_VIEWS, WIKI_PAGE_VIEWS_DUMP_DIR
from collections import Counter
from calendar import monthrange


GET_URL = lambda year, month, day, hour: f"https://dumps.wikimedia.org/other/pageviews/{year}/{year}-{month:02d}/{GET_FILE_NAME(year, month, day, hour)}.gz"
GET_FILE_NAME = lambda year, month, day, hour: f"pageviews-{year}{month:02d}{day:02d}-{hour:02d}0000"
GET_ZIPPED_FILE_NAME = lambda year, month, day, hour: f"{GET_FILE_NAME(year, month, day, hour)}.gz"

DOWNLOAD_BATCH_SIZE = 10

YEAR = 2021
MONTHS = 12
DAY_STEP = 4
HOURS_PER_DAY = 24
HOUR_STEP = 4

def get_timestamps_to_process():
    timestamps = []

    for m in range(1, MONTHS + 1):
        days_in_month = monthrange(YEAR, m)[1]
        for d in range(1, days_in_month + 1, DAY_STEP):
            for h in range(0, HOURS_PER_DAY, HOUR_STEP):
                timestamps.append((YEAR, m, d, h))
    
    return timestamps


def timestamp_needs_download(timestamp):
    file_name = GET_FILE_NAME(*timestamp)
    return not os.path.isfile(os.path.join(WIKI_PAGE_VIEWS_DUMP_DIR, file_name))


def download_page_views(timestamps):
    undownloaded_timestamps = list(filter(timestamp_needs_download, timestamps))

    print("Downloading timestamps", "Total:", len(timestamps), "Downloading:", len(undownloaded_timestamps))

    with tqdm(total=len(undownloaded_timestamps)) as pbar:
        for i in range(0, len(undownloaded_timestamps), DOWNLOAD_BATCH_SIZE):
            batch_timestamps = undownloaded_timestamps[i:i + DOWNLOAD_BATCH_SIZE]

            batch_urls = [GET_URL(*timestamp) for timestamp in batch_timestamps]
            procs = [command(["wget", url], WIKI_PAGE_VIEWS_DUMP_DIR) for url in batch_urls]
            for proc in procs:
                proc.wait()
            
            batch_zipped_files = [GET_ZIPPED_FILE_NAME(*timestamp) for timestamp in batch_timestamps]
            procs = [command(["gzip", "-d", batch_zipped_files], WIKI_PAGE_VIEWS_DUMP_DIR) for zipped_file in batch_zipped_files]
            for proc in procs:
                proc.wait()
            
            pbar.update(DOWNLOAD_BATCH_SIZE)


def parse_page_views(timestamp):
    file_name = GET_FILE_NAME(*timestamp)

    with open(os.path.join(WIKI_PAGE_VIEWS_DUMP_DIR, file_name), "r") as file:
        lines = file.read().splitlines()
        lines = filter(lambda line: line.startswith("en"), lines)
        lines = [line.split(" ") for line in lines]
        page_views = {line[1]: int(line[2]) for line in lines}

    return Counter(page_views)


def command(command, cwd):
    return subprocess.Popen(
        command,
        cwd=cwd,
        shell=False,
    )


def main():
    start_time = time.time()

    timestamps = get_timestamps_to_process()    
    download_page_views(timestamps)
    page_views = Counter()

    for timestamp in tqdm(timestamps):
        page_views.update(parse_page_views(timestamp))
    
    with open(WIKI_PAGE_VIEWS, "w+") as file:
        file.write("\n".join(list(map(lambda item: item[0] + " " + str(item[1]), page_views.items()))))
    
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
