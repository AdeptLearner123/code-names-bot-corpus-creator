import os

from config import PREMIUM_OXFORD_WORD_LIST_DIR_US, PREMIUM_OXFORD_WORD_LIST_DIR_WORLD
from .oxford_definitions import OxfordDefinitions
from tqdm import tqdm


def main():
    terms_us = set()
    for file_name in os.listdir(PREMIUM_OXFORD_WORD_LIST_DIR_US):
        with open(os.path.join(PREMIUM_OXFORD_WORD_LIST_DIR_US, file_name), "r") as file:
            terms_us = terms_us.union(set(file.read().splitlines()))
    terms_us = set(map(lambda term: term.lower(), terms_us))

    terms_world = set()
    for file_name in os.listdir(PREMIUM_OXFORD_WORD_LIST_DIR_WORLD):
        with open(os.path.join(PREMIUM_OXFORD_WORD_LIST_DIR_WORLD, file_name), "r") as file:
            terms_world = terms_world.union(set(file.read().splitlines()))
    terms_world = set(map(lambda term: term.lower(), terms_world))

    oxford_definitions = OxfordDefinitions()
    oxford_definitions.setup()

    for term in tqdm(terms_us):
        oxford_definitions.insert_term(term, True)

    for term in tqdm(terms_world.difference(terms_us)):
        oxford_definitions.insert_term(term, False)

    oxford_definitions.commit()


if __name__ == "__main__":
    main()
