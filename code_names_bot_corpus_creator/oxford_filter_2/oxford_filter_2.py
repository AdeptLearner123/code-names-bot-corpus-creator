from config import OXFORD_FILTERED_1, OXFORD_FILTERED_2, MISSING_SENTENCES

def main():
    with open(OXFORD_FILTERED_1, "r") as file:
        lemma_regions = file.read().splitlines()

    with open(MISSING_SENTENCES) as file:
        missing_sentences = set(file.read().splitlines())

    lemma_regions = filter(lambda lemma_region: lemma_region.split("|")[0] not in missing_sentences, lemma_regions)
    
    with open(OXFORD_FILTERED_2, "w+") as file:
        file.write("\n".join(lemma_regions))


if __name__ == "__main__":
    main()
