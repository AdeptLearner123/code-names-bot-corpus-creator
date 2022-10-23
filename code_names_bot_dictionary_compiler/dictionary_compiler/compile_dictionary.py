from config import WIKI_FILTERED_4, OXFORD_FILTERED_3, COMPILED_DICTIONARY

import json


def main():
    with open(OXFORD_FILTERED_3, "r") as file:
        oxford_dictionary = json.loads(file.read())

    with open(WIKI_FILTERED_4, "r") as file:
        wiki_dictionary = json.loads(file.read())

    oxford_dictionary.update(wiki_dictionary)

    with open(COMPILED_DICTIONARY, "w+") as file:
        file.write(json.dumps(oxford_dictionary, sort_keys=True, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
