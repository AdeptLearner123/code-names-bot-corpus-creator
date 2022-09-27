import requests
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed


def download(
    keys,
    get_request_params,
    cache,
    process_result,
    chunk_size,
    download_rate,
):
    cached_keys = set(cache.get_cached_keys())
    target_keys = list(filter(lambda key: key not in cached_keys, keys))

    print("Total keys: ", len(keys), "Target keys: ", len(target_keys))

    start_time = time.time()

    with tqdm(total=len(target_keys)) as pbar:
        for i in range(0, len(target_keys), chunk_size):
            target_chunk = target_keys[i : i + chunk_size]
            results = dict()

            with ThreadPoolExecutor(max_workers=len(target_chunk)) as ex:
                futures = [
                    ex.submit(
                        download_result,
                        key,
                        get_request_params(key),
                        results,
                    )
                    for key in target_chunk
                ]
                for _ in as_completed(futures):
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

            time.sleep(chunk_size / download_rate)

    print("--- %s seconds ---" % (time.time() - start_time))


def download_result(key, request_params, results):
    r = requests.get(**request_params)
    results[key] = r
