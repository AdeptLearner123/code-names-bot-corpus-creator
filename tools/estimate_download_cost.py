from code_names_bot_corpus_creator.caches.oxford_cache import OxfordCache
from config import FILTERED_LEMMAS


def main():
    with open(FILTERED_LEMMAS, "r") as file:
        lemmas = set(file.read().splitlines())

    oxford_cache = OxfordCache()
    cached_terms = set(oxford_cache.get_all_cached())
    uncached = lemmas.difference(cached_terms)

    print("Total lemmas", len(lemmas))
    print("Uncached", len(uncached))
    print("Estimated cost", get_cost(len(uncached)))


def get_cost(count):
    cost = 0.0022 * min(count, 10000)
    count -= 10000

    cost += 0.0011 * max(0, min(count, 90000))
    count -= 90000

    cost += 0.0006 * max(0, count)

    return cost * 1.15


if __name__ == "__main__":
    main()
