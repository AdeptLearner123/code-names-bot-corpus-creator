import requests
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed


def download(
    keys,
    cache,
    process_result,
    chunk_size,
    download_rate,
    get_request_params=None,
    make_request=None,
):
    cached_keys = set(cache.get_cached_keys())
    target_keys = list(filter(lambda key: key not in cached_keys, keys))
    print("Total keys: ", len(keys), "Target keys: ", len(target_keys))

    if make_request is None:
        download_task = lambda key: (key, requests.get(**get_request_params(key)))
    else:
        download_task = make_request

    start_time = time.time()

    with tqdm(total=len(target_keys)) as pbar:
        for i in range(0, len(target_keys), chunk_size):
            target_chunk = target_keys[i : i + chunk_size]
            results = dict()
            chunk_start_time = time.time()

            with ThreadPoolExecutor(max_workers=len(target_chunk)) as ex:
                futures = [
                    ex.submit(
                        download_task,
                        key,
                    )
                    for key in target_chunk
                ]
                for future in as_completed(futures):
                    key, result = future.result()
                    results[key] = result
                    pbar.update(1)

            chunk_failed = 0
            for key in target_chunk:
                if key not in results:
                    print("Key not in results", key)
                    chunk_failed += 1
                    continue

                result, should_continue = process_result(key, results[key])

                if not should_continue:
                    chunk_failed += 1
                    continue

                if result is not None:
                    cache.cache_value(key, result)

            cache.commit()

            if chunk_failed > 0:
                print("Chunk Failed", chunk_failed)
                break

            chunk_time_elapsed = time.time() - chunk_start_time
            sleep_time = chunk_size / download_rate - chunk_time_elapsed
            if sleep_time > 0:
                time.sleep(chunk_size / download_rate - chunk_time_elapsed)

    print("--- %s seconds ---" % (time.time() - start_time))
