import os

from code_names_bot_corpus_creator.caches.oxford_cache import OxfordCache
from config import FILTERED_LEMMAS


def main():
    oxford_cache = OxfordCache()

    with open(FILTERED_LEMMAS, "r") as file:
        lemma_regions = file.read().splitlines()
        lemmas = list(
            map(lambda lemma_region: lemma_region.split("|")[0], lemma_regions)
        )

    for lemma in lemmas:
        oxford_cache.insert_query(lemma)

    oxford_cache.commit()


if __name__ == "__main__":
    main()
