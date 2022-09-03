import os

from config import WORDLIST_PATH, PREMIUM_OXFORD_WORD_LIST_DIR_US, PREMIUM_OXFORD_WORD_LIST_DIR_WORLD

WORD_FREQ_THRESHOLD = 1e-6


def main():
    lemmas = set()
    for file_name in os.listdir(PREMIUM_OXFORD_WORD_LIST_DIR_US):
        with open(os.path.join(PREMIUM_OXFORD_WORD_LIST_DIR_US, file_name), "r") as file:
            lemmas += set(file.read().splitlines())

    for file_name in os.listdir(PREMIUM_OXFORD_WORD_LIST_DIR_WORLD):
        with open(os.path.join(PREMIUM_OXFORD_WORD_LIST_DIR_US, file_name), "r") as file:
            lemmas += set(file.read().splitlines())
    
    lemmas = list(lemmas)

    with open(WORDLIST_PATH, "w+") as file:
        file.write("\n".join(lemmas))


if __name__ == "__main__":
    main()
