import os

from wordfreq import word_frequency

from config import FILTERED_LEMMAS, ALL_LEMMAS

FREQUENCY_THRESHOLD = 1e-6


def main():
    with open(ALL_LEMMAS, "r") as file:
        lemma_regions = file.read().splitlines()

    lemma_regions = filter(
        lambda lemma_region: word_frequency(lemma_region.split("|")[0], "en")
        > FREQUENCY_THRESHOLD,
        lemma_regions,
    )
    lemma_regions = list(lemma_regions)

    with open(FILTERED_LEMMAS, "w+") as file:
        file.write("\n".join(lemma_regions))


if __name__ == "__main__":
    main()
