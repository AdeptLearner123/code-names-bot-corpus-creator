from code_names_bot_dictionary_compiler.download.caches import (
    OxfordDefinitionsCache,
    OxfordSentencesCache,
)

from code_names_bot_dictionary_compiler.utils.spacy_utils import split_format_sentences
from code_names_bot_dictionary_compiler.oxford_utils.sense_iterator import iterate_senses

from config import OXFORD_FILTERED_1, OXFORD_FILTERED_2

import json

CONTENT_POS = set(["noun", "proper", "verb", "adjective", "adverb"])


def get_filtered_senses(definitions_cache):
    sense_ids = set()
    for lexical_entry, _, sense, _ in iterate_senses(definitions_cache):
        sense_id = sense["id"]
        lexical_category = lexical_entry["lexicalCategory"]["id"]
        if lexical_category in CONTENT_POS:
            sense_ids.add(sense_id)
    return list(sense_ids)


def extract_sense_data(sense_json):
    # NOTE: Some definitions have multiple sentences, such as for "Scandinavia"
    definition = sense_json["definitions"][0]
    texts = split_format_sentences(definition)
    definition = texts[0]
    texts = texts[1:]

    return (definition, texts)


def format_lemma(lemma):
    if ", " in lemma:
        # Names should be converted from Last, First to First Last
        parts = lemma.split(", ")
        return parts[1] + " " + parts[0]
    return lemma


def create_dictionary(filtered_senses):
    definitions_cache = OxfordDefinitionsCache()
    definitions = dict()

    for lexical_entry, entry, sense, _ in iterate_senses(definitions_cache):
        sense_id = sense["id"]
        if sense_id not in filtered_senses:
            continue

        lemma_text = lexical_entry["text"]

        notes = []
        if "notes" in entry:
            for note in entry["notes"]:
                if note["type"] == "encyclopedicNote":
                    notes += split_format_sentences(note["text"])

        sense_data = extract_sense_data(sense)

        if sense_data is not None:
            (
                definition,
                texts
            ) = sense_data
            
            definitions[sense_id] = {
                "lemma": format_lemma(lemma_text),
                "source": "OX",
                "definition": definition,
                "texts": texts + notes
            }

    return definitions


def main():
    with open(OXFORD_FILTERED_1, "r") as file:
        lemma_regions = file.read().splitlines()
        lemmas = [lemma_region.split("|")[0] for lemma_region in lemma_regions]

    definitions_cache = OxfordDefinitionsCache()

    print("Status:", "filtering")
    filtered_senses = get_filtered_senses(definitions_cache)

    print("Status:", "creating dictionary")
    dictionary = create_dictionary(filtered_senses)

    print("Total senses", len(dictionary))

    with open(OXFORD_FILTERED_2, "w+") as file:
        file.write(json.dumps(dictionary, sort_keys=True, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
