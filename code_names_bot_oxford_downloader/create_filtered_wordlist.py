import os
from tqdm import tqdm
from wordfreq import word_frequency

from config import WORDLIST_PATH, FILTERED_WORDLIST_PATH
from .oxford_definitions import OxfordDefinitions

FREQUENCY_THRESHOLD = 1e-5

def main():
    with open(WORDLIST_PATH, "r") as file:
        lemmas = list(file.read().splitlines())
    
    lemmas = map(lambda lemma: lemma.lower(), lemmas)
    lemmas = filter(lambda lemma: word_frequency(lemma, "en") > FREQUENCY_THRESHOLD, lemmas)
    lemmas = set(lemmas)

    with open(FILTERED_WORDLIST_PATH, "w+") as file:
        file.write("\n".join(lemmas))

    oxford_definitions = OxfordDefinitions()
    cached_terms = set(oxford_definitions.get_all_cached())
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
