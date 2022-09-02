import os

from nltk.corpus import wordnet as wn
from wordfreq import word_frequency

from config import COMPOUNDS_LIST_PATH, OXFORD_WORD_LIST_DIR

WORD_FREQ_THRESHOLD = 1e-6


def main():
    lemmas = []
    for file_name in os.listdir(OXFORD_WORD_LIST_DIR):
        with open(os.path.join(OXFORD_WORD_LIST_DIR, file_name), "r") as file:
            lemmas += file.read().splitlines()

    compounds = list(filter(lambda lemma: " " in lemma, lemmas))

    with open(COMPOUNDS_LIST_PATH, "w+") as file:
        file.write("\n".join(compounds))


if __name__ == "__main__":
    main()
