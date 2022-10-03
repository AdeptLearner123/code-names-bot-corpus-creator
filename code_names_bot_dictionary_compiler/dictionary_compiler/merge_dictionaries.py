from config import WIKI_FILTERED_4, OXFORD_FILTERED_2

import yaml

WIKI_PAGE_VIEWS_THRESHOLD = 750000
OXFORD_SENTENCES_THRESHOLD = 3


def augment_wiki_dictionary(filtered_wiki_dict, oxford_dict):



def main():
    with open(WIKI_FILTERED_4, "r") as file:
        wiki_dict = yaml.safe_load(file)

    with open(OXFORD_FILTERED_2, "r") as file:
        oxford_dict = yaml.safe_load(file)

    filtered_wiki_dict = {
        title: wiki_dict[title]
        for title in wiki_dict
        if wiki_dict[title]["views"] > WIKI_PAGE_VIEWS_THRESHOLD
        and wiki_dict[title]["pos"] == "proper"
    }
    filtered_oxford_dict = {
        lemma: oxford_dict[lemma]
        for lemma in oxford_dict
        if oxford_dict[lemma]["sentences"] > OXFORD_SENTENCES_THRESHOLD
        and oxford_dict[lemma]["pos"] != "proper"
    }


if __name__ == "__main__":
    main()
