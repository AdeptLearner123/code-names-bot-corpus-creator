from code_names_bot_dictionary_compiler.download.caches import (
    OxfordDefinitionsCache,
    OxfordSentencesCache,
)

from code_names_bot_dictionary_compiler.utils.spacy_utils import split_sentences, format_sentence_text
from code_names_bot_dictionary_compiler.oxford_utils.sense_iterator import iterate_senses

from config import OXFORD_FILTERED_1, OXFORD_FILTERED_2

from tqdm import tqdm
import json
from collections import defaultdict

CONTENT_POS = set(["noun", "proper", "verb", "adjective", "adverb"])
SENTENCE_COUNT_THRESHOLD = 4

# This is for lemmas that don't have example sentences but are commonly known
MANUAL_INCLUDE = set(["scuba diver"])


def get_sense_sentence_counts(lemmas):
    sentences_cache = OxfordSentencesCache()
    query_to_result = sentences_cache.get_key_to_value()
    sentence_counts = defaultdict(lambda: 0)

    for lemma in lemmas:
        if lemma not in query_to_result:
            continue

        results_str = query_to_result[lemma]
        results = json.loads(results_str)
        for result in results["results"]:
            for lexical_entry in result["lexicalEntries"]:
                for sentence in lexical_entry["sentences"]:
                    for sense_id in set(sentence["senseIds"]):
                        sentence_counts[sense_id] += 1

    return sentence_counts


def extract_sense_data(text, sense_json):
    sense_id = sense_json["id"]
    # NOTE: Some definitions have multiple sentences, such as for "Scandinavia"
    definition = sense_json["definitions"][0]
    texts = split_sentences(definition)
    texts = [ format_sentence_text(text) for text in texts ]
    definition = texts[0]
    texts = texts[1:]

    return (sense_id, definition, texts)


def format_lemma(lemma):
    if ", " in lemma:
        # Names should be converted from Last, First to First Last
        parts = lemma.split(", ")
        return parts[1] + " " + parts[0]
    return lemma


def get_sense_definitions(lemmas):
    definitions_cache = OxfordDefinitionsCache()
    definitions = dict()

    for lexical_entry, entry, sense, _ in iterate_senses(definitions_cache, tqdm(lemmas)):
        lemma_text = lexical_entry["text"]
        lexical_category = lexical_entry["lexicalCategory"]["id"]

        grammatical_features = []
        if "grammaticalFeatures" in entry:
            grammatical_features = set([ item["id"] for item in entry["grammaticalFeatures"] ])

        pos = (
            "proper"
            if "proper" in grammatical_features
            else lexical_category
        )

        notes = []
        if "notes" in entry:
            for note in entry["notes"]:
                if note["type"] == "encyclopedicNote":
                    notes += split_sentences(note["text"])
        notes = [ format_sentence_text(note) for note in notes ]

        sense_data = extract_sense_data(lemma_text, sense)

        if sense_data is not None:
            (
                sense_id,
                definition,
                texts
            ) = sense_data
            
            definitions[sense_id] = {
                "lemma": format_lemma(lemma_text),
                "source": "OX",
                "pos": pos,
                "definition": definition,
                "texts": texts + notes
            }

    return definitions


def main():
    with open(OXFORD_FILTERED_1, "r") as file:
        lemma_regions = file.read().splitlines()
        lemmas = [lemma_region.split("|")[0] for lemma_region in lemma_regions]

    print("Status:", "get sentence counts")
    sentence_counts = get_sense_sentence_counts(lemmas)
    print("Status:", "get sentence definitions")
    definitions = get_sense_definitions(lemmas)

    print("Status:", "filtering lemmas")
    sense_ids = definitions.keys()

    sense_ids = list(
        filter(
            lambda sense_id: definitions[sense_id]["pos"] == "proper"
            or (
                definitions[sense_id]["pos"] in CONTENT_POS
                and (
                    sentence_counts[sense_id] >= SENTENCE_COUNT_THRESHOLD
                    or definitions[sense_id]["lemma"] in MANUAL_INCLUDE
                )
            ),
            sense_ids,
        )
    )

    filtered_definitions = {sense_id: definitions[sense_id] for sense_id in sense_ids}

    print("Total senses", len(sense_ids))

    with open(OXFORD_FILTERED_2, "w+") as file:
        file.write(json.dumps(filtered_definitions, sort_keys=True, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
