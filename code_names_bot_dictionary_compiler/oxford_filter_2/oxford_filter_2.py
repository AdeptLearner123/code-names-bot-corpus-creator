from code_names_bot_dictionary_compiler.download.caches import (
    OxfordDefinitionsCache,
    OxfordSentencesCache,
)

from code_names_bot_dictionary_compiler.utils.spacy_utils import split_format_sentences
from code_names_bot_dictionary_compiler.oxford_utils.sense_iterator import iterate_senses

from config import OXFORD_FILTERED_1, OXFORD_FILTERED_2

from tqdm import tqdm
import json
from collections import defaultdict

CONTENT_POS = set(["noun", "proper", "verb", "adjective", "adverb"])
SENTENCE_COUNT_THRESHOLD = 4

# This is for lemmas that don't have example sentences but are commonly known
MANUAL_INCLUDE = set([
    "m_en_gbus1189026.002"  # scuba diver
])


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


def get_sense_pos(definitions_cache):
    sense_pos = dict()
    for lexical_entry, entry, sense, _ in iterate_senses(definitions_cache):
        sense_id = sense["id"]
        lexical_category = lexical_entry["lexicalCategory"]["id"]

        grammatical_features = []
        if "grammaticalFeatures" in entry:
            grammatical_features = set([ item["id"] for item in entry["grammaticalFeatures"] ])

        sense_pos[sense_id] = "proper" if "proper" in grammatical_features else lexical_category
    return sense_pos


def get_filtered_senses(sentence_counts, sense_pos):
    sense_ids = []

    for sense_id, pos in sense_pos.items():        
        if sense_id in MANUAL_INCLUDE or pos == "proper" or (pos in CONTENT_POS and sentence_counts[sense_id] >= SENTENCE_COUNT_THRESHOLD):
            sense_ids.append(sense_id)
    
    return sense_ids


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


def create_dictionary(filtered_senses, sense_pos, sentence_counts):
    definitions_cache = OxfordDefinitionsCache()
    definitions = dict()

    for lexical_entry, entry, sense, _ in iterate_senses(definitions_cache):
        sense_id = sense["id"]
        if sense_id not in filtered_senses:
            continue

        pos = sense_pos[sense_id]
        sentence_count = sentence_counts[sense_id]

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
                "pos": pos,
                "definition": definition,
                "texts": texts + notes,
                "meta": {
                    "sentence_count": sentence_count
                }
            }

    return definitions


def main():
    with open(OXFORD_FILTERED_1, "r") as file:
        lemma_regions = file.read().splitlines()
        lemmas = [lemma_region.split("|")[0] for lemma_region in lemma_regions]

    definitions_cache = OxfordDefinitionsCache()

    print("Status:", "get sentence counts")
    sentence_counts = get_sense_sentence_counts(lemmas)

    print("Status:", "get sense pos")
    sense_pos = get_sense_pos(definitions_cache)

    print("Status:", "filtering")
    filtered_senses = get_filtered_senses(sentence_counts, sense_pos)

    print("Status:", "creating dictionary")
    dictionary = create_dictionary(filtered_senses, sense_pos, sentence_counts)

    print("Total senses", len(dictionary))

    with open(OXFORD_FILTERED_2, "w+") as file:
        file.write(json.dumps(dictionary, sort_keys=True, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
