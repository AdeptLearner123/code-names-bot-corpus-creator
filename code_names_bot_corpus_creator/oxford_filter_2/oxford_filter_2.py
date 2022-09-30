from config import OXFORD_FILTERED_1, OXFORD_FILTERED_2, MISSING_SENTENCES

def main():
    with open(OXFORD_FILTERED_1, "r") as file:
        lemma_regions = file.read().splitlines()
        lemmas = [lemma_region.split("|")[0] for lemma_region in lemma_regions ]

    with open(MISSING_SENTENCES) as file:
        missing_sentences = set(file.read().splitlines())

    lemmas = filter(lambda lemma: lemma not in missing_sentences)
    
    with open(OXFORD_FILTERED_2, "w+") as file:
        file.write("\n".join(lemmas))


if __name__ == "__main__":
    main()
