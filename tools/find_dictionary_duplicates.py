from tqdm import tqdm
import yaml

from config import WIKI_FILTERED_4, OXFORD_FILTERED_2


def main():
    with open(WIKI_FILTERED_4) as file:
        wiki_entries = yaml.safe_load(file.read())
        wiki_dict = set()
        for title in tqdm(wiki_entries):
            text = wiki_entries[title]["text"]
            if text in wiki_dict:
                print("Duplicate text", text)
            wiki_dict.add(text)

    print("Wiki entries", len(wiki_entries))
    print("Total unique wiki lemmas", len(wiki_dict))

    with open(OXFORD_FILTERED_2) as file:
        oxford_entries = yaml.safe_load(file.read())
        proper_lemmas = set()
        for lemma in tqdm(oxford_entries):
            if oxford_entries[lemma]["pos"] == "proper":
                text = oxford_entries[lemma]["text"]
                if text in proper_lemmas:
                    print("Duplicate oxford lemma", text)
                proper_lemmas.add(text)

    print("Oxford entries", len(oxford_entries))
    print("Total oxford proper noun entries", len(proper_lemmas))


if __name__ == "__main__":
    main()
