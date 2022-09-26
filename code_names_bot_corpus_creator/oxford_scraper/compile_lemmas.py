import os

from config import ALL_LEMMAS, SCRAPED_LEMMAS_US_DIR, SCRAPED_LEMMAS_WORLD_DIR


def main():
    lemmas = set()
    lemma_to_region = dict()

    for file_name in os.listdir(SCRAPED_LEMMAS_WORLD_DIR):
        with open(os.path.join(SCRAPED_LEMMAS_WORLD_DIR, file_name), "r") as file:
            world_lemmas = file.read().splitlines()
            world_lemmas = set(map(lambda lemma: lemma.lower(), world_lemmas))
            lemmas = lemmas.union(world_lemmas)

            for lemma in world_lemmas:
                lemma_to_region[lemma] = "world"

    for file_name in os.listdir(SCRAPED_LEMMAS_US_DIR):
        with open(os.path.join(SCRAPED_LEMMAS_US_DIR, file_name), "r") as file:
            us_lemmas = file.read().splitlines()
            us_lemmas = set(map(lambda lemma: lemma.lower(), us_lemmas))
            lemmas = lemmas.union(us_lemmas)

            for lemma in us_lemmas:
                lemma_to_region[lemma] = "us"

    lemmas = map(lambda lemma: f"{lemma}|{lemma_to_region[lemma]}", lemmas)
    lemmas = list(lemmas)

    with open(ALL_LEMMAS, "w+") as file:
        file.write("\n".join(lemmas))


if __name__ == "__main__":
    main()
