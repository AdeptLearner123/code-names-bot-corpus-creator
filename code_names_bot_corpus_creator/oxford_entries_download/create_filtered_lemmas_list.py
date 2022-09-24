import os

from wordfreq import word_frequency

from config import (FILTERED_LEMMAS, SCRAPED_LEMMAS_US_DIR,
                    SCRAPED_LEMMAS_WORLD_DIR)

FREQUENCY_THRESHOLD = 1e-5


def main():
    lemmas = set()
    for file_name in os.listdir(SCRAPED_LEMMAS_US_DIR):
        with open(os.path.join(SCRAPED_LEMMAS_US_DIR, file_name), "r") as file:
            lemmas = lemmas.union(set(file.read().splitlines()))

    for file_name in os.listdir(SCRAPED_LEMMAS_WORLD_DIR):
        with open(os.path.join(SCRAPED_LEMMAS_WORLD_DIR, file_name), "r") as file:
            lemmas = lemmas.union(set(file.read().splitlines()))

    lemmas = list(lemmas)
    lemmas = map(lambda lemma: lemma.lower(), lemmas)
    lemmas = filter(
        lambda lemma: word_frequency(lemma, "en") > FREQUENCY_THRESHOLD, lemmas
    )
    lemmas = set(lemmas)

    with open(FILTERED_LEMMAS, "w+") as file:
        file.write("\n".join(lemmas))


if __name__ == "__main__":
    main()
