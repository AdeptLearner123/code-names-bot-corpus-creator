from config import WIKI_FILTERED_4, OXFORD_FILTERED_2, COMPILED_DICTIONARY

import yaml


def main():
    with open(OXFORD_FILTERED_2, "r") as file:
        oxford_dictionary = yaml.safe_load(file.read())
    
    with open(WIKI_FILTERED_4, "r") as file:
        wiki_dictionary = yaml.safe_load(file.read())

    oxford_dictionary.update(wiki_dictionary)    

    with open(COMPILED_DICTIONARY, "w+") as file:
        yaml.dump(oxford_dictionary, file, sort_keys=True, allow_unicode=True)
 

if __name__ == "__main__":
    main()
