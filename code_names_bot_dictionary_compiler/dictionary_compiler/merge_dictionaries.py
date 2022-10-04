from config import WIKI_FILTERED_4, OXFORD_FILTERED_2, MERGED_DICTIONARY

import yaml
from collections import defaultdict

WIKI_PAGE_VIEWS_THRESHOLD = 750000
OXFORD_SENTENCES_THRESHOLD = 3

def process_dict(dictionary):
    for title in dictionary:
        entry = dictionary[title]
        entry["definitions"] = [ entry["definition"] ]
        del entry["definition"]
        #if "views" in entry:
        #    del entry["views"]
        #else:
        #    del entry["sentences"]


def augment_wiki_dictionary(filtered_wiki_dict, oxford_dict):
    oxford_proper_map = defaultdict(lambda: [])

    for lemma in oxford_dict:
        if oxford_dict[lemma]["pos"] == "proper":
            oxford_proper_map[oxford_dict[lemma]["text"]].append(oxford_dict[lemma])
    
    wiki_proper_counts = defaultdict(lambda: 0)
    for title in filtered_wiki_dict:
        wiki_proper_counts[filtered_wiki_dict[title]["text"]] += 1

    for title in filtered_wiki_dict:
        text = filtered_wiki_dict[title]["text"]
        
        if text not in oxford_proper_map:
            continue

        if wiki_proper_counts[text] > 1:
            print(f"Can't augment {title} because multiple Wikipedia proper entries for {text}")
        
        if len(oxford_proper_map[text]) > 1:
            print(f"Can't augment {title} because multiple Oxford proper entries for {text}")

        filtered_wiki_dict[title]["definitions"].append(oxford_proper_map[text][0]["definition"])


def augment_oxford_dictionary(filtered_oxford_dict, wiki_dict):
    oxford_nouns = dict()

    for sense_id in filtered_oxford_dict:
        if filtered_oxford_dict[sense_id]["pos"] != "noun":
            continue

        text = filtered_oxford_dict[sense_id]["text"]
        sentences = filtered_oxford_dict[sense_id]["sentences"]
        if text not in oxford_nouns or sentences > oxford_nouns[text][1]:
            oxford_nouns[text] = (sense_id, sentences)

    wiki_common_nouns = defaultdict(lambda: [])
    for title in wiki_dict:
        text = wiki_dict[title]["text"]
        if wiki_dict[title]["pos"] == "noun":
            wiki_common_nouns[text].append(wiki_dict[title])

    for text in oxford_nouns:
        if text not in wiki_common_nouns:
            continue

        if len(wiki_common_nouns) > 1:
            print(f"Can't augment {text} because multiple Wikipedia common entries for {text}")
        
        sense_id = oxford_nouns[text][0]
        filtered_oxford_dict[sense_id]["definitions"].append(wiki_common_nouns[text][0]["definition"])


def main():
    print("Status:", "reading files")
    with open(WIKI_FILTERED_4, "r") as file:
        wiki_dict = yaml.safe_load(file)

    with open(OXFORD_FILTERED_2, "r") as file:
        oxford_dict = yaml.safe_load(file)

    print("Status:", "filtering")
    filtered_wiki_dict = {
        title: wiki_dict[title]
        for title in wiki_dict
        if wiki_dict[title]["views"] > WIKI_PAGE_VIEWS_THRESHOLD
        and wiki_dict[title]["pos"] == "proper"
    }
    process_dict(filtered_wiki_dict)

    filtered_oxford_dict = {
        lemma: oxford_dict[lemma]
        for lemma in oxford_dict
        if oxford_dict[lemma]["sentences"] > OXFORD_SENTENCES_THRESHOLD
        and oxford_dict[lemma]["pos"] != "proper"
    }
    process_dict(filtered_oxford_dict)

    print("Status:", "augmenting wiki dict")
    #augment_wiki_dictionary(filtered_wiki_dict, oxford_dict)
    print("Status:", "augmenting oxford dict")
    augment_oxford_dictionary(filtered_oxford_dict, wiki_dict)

    print("Status:", "merging")
    merged_dict = filtered_wiki_dict.update(filtered_oxford_dict)

    print("Status:", "writing")
    with open(MERGED_DICTIONARY, "w+") as file:
        yaml.dump(merged_dict, file)


if __name__ == "__main__":
    main()
