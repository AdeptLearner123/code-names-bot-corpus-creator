import yaml

from config import COMPILED_DICTIONARY, CODE_NAMES_LEMMAS

def main():
    with open(COMPILED_DICTIONARY, "r") as file:
        dictionary = yaml.safe_load(file)
        lemmas = []
        for entry in dictionary.values():
            lemmas += [entry["lemma"]] + entry["variants"]
        lemmas = set(map(lambda lemma: lemma.lower(), lemmas))
    
    with open(CODE_NAMES_LEMMAS, "r") as file:
        code_names_lemmas = file.read().splitlines()
        code_names_lemmas = [ lemma.lower() for lemma in code_names_lemmas ]

    missing_lemmas = list(filter(lambda lemma: lemma not in lemmas, code_names_lemmas))

    for lemma in missing_lemmas:
        print("Missing Code Names word", lemma)


if __name__ == "__main__":
    main()