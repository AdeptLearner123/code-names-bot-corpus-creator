import os

from nltk.corpus import wordnet as wn
from wordfreq import word_frequency

from config import OXFORD_WORD_LIST_DIR, TARGET_LEMMA_LISTS

WORD_FREQ_THRESHOLD = 1e-6


def save_lemmas(lemmas, length, file_name):
    filtered = filter(lambda lemma: len(lemma.split(" ")) == length, lemmas)
    filtered = filter(
        lambda lemma: not any(char.isdigit() or char in [".", "'"] for char in lemma),
        filtered,
    )
    filtered = filter(
        lambda lemma: word_frequency(lemma, "en") > WORD_FREQ_THRESHOLD, filtered
    )
    filtered = list(filtered)

    with open(os.path.join(TARGET_LEMMA_LISTS, file_name), "w+") as file:
        for lemma in filtered:
            file.write(lemma + "\n")

    return len(filtered)


def main():
    lemmas = []
    for file_name in os.listdir(OXFORD_WORD_LIST_DIR):
        with open(os.path.join(OXFORD_WORD_LIST_DIR, file_name), "r") as file:
            lemmas += file.read().splitlines()

    total = 0
    total += save_lemmas(lemmas, 1, "wordnet_lemmas_1")
    total += save_lemmas(lemmas, 2, "wordnet_lemmas_2")
    total += save_lemmas(lemmas, 3, "wordnet_lemmas_3")

    print("All lemmas: ", len(lemmas))
    print("Target lemmas: ", total)


if __name__ == "__main__":
    main()
