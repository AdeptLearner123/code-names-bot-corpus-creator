from code_names_bot_dictionary_compiler.download.caches import (
    OxfordDefinitionsCache,
    OxfordSentencesCache,
)

from code_names_bot_dictionary_compiler.utils.spacy_utils import split_sentences

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
    if "id" not in sense_json or "definitions" not in sense_json:
        return None

    sense_id = sense_json["id"]
    definition = sense_json["definitions"][0]
    texts = split_sentences(definition)
    definition = texts[0]
    texts = texts[1:]
    synonyms, domains, variant_forms = [], [], []

    if "domainClasses" in sense_json:
        domains = [domain_class["id"] for domain_class in sense_json["domainClasses"]]

    if "synonyms" in sense_json:
        synonyms = [synonym["text"] for synonym in sense_json["synonyms"]]
        if text in synonyms:
            synonyms.remove(text)
    
    if "variantForms" in sense_json:
        variant_forms = [variant_form["text"] for variant_form in sense_json["variantForms"]]

    return (sense_id, definition, texts, synonyms, domains, variant_forms)


def format_lemma(lemma):
    if ", " in lemma:
        # Names should be converted from Last, First to First Last
        parts = lemma.split(", ")
        return parts[1] + " " + parts[0]
    return lemma


def get_sense_definitions(lemmas):
    definitions_cache = OxfordDefinitionsCache()
    definitions = dict()
    query_to_result = definitions_cache.get_key_to_value()

    for lemma in tqdm(lemmas):
        if lemma not in query_to_result:
            continue

        results_str = query_to_result[lemma]
        results = json.loads(results_str)
        for result in results["results"]:
            for lexical_entry in result["lexicalEntries"]:
                text = lexical_entry["text"]
                lexical_category = lexical_entry["lexicalCategory"]["id"]

                for entry in lexical_entry["entries"]:
                    grammatical_features = []
                    if "grammaticalFeatures" in entry:
                        grammatical_features = set(
                            [
                                grammatical_feature["id"]
                                for grammatical_feature in entry["grammaticalFeatures"]
                            ]
                        )

                    notes = []
                    if "notes" in entry:
                        for note in entry["notes"]:
                            if note["type"] == "encyclopedicNote":
                                notes += split_sentences(note["text"])

                    variants = []
                    if "inflections" in entry:
                        variants += [
                            inflection["inflectedForm"]
                            for inflection in entry["inflections"]
                        ]

                    if "variantForms" in entry:
                        variants += list(
                            set(
                                [
                                    variantForm["text"]
                                    for variantForm in entry["variantForms"]
                                ]
                            )
                        )

                    variants = set(variants)
                    if text in variants:
                        variants.remove(text)
                    variants = list(variants)

                    pos = (
                        "proper"
                        if "proper" in grammatical_features
                        else lexical_category
                    )

                    if "senses" in entry:
                        for sense in entry["senses"]:
                            sense_data = extract_sense_data(text, sense)

                            if sense_data is not None:
                                (
                                    sense_id,
                                    definition,
                                    texts,
                                    synonyms,
                                    domains,
                                    sense_variants
                                ) = sense_data
                                
                                definitions[sense_id] = {
                                    "lemma": format_lemma(text),
                                    "pos": pos,
                                    "definition": definition,
                                    "texts": texts + notes,
                                    "synonyms": synonyms,
                                    "variants": variants + sense_variants,
                                    "domains": domains,
                                    "source": "OX",
                                }

                            if "subsenses" in sense:
                                for subsense in sense["subsenses"]:
                                    subsense_data = extract_sense_data(text, subsense)

                                    if subsense_data is not None:
                                        (
                                            subsense_id,
                                            definition,
                                            texts,
                                            synonyms,
                                            domains,
                                            sense_variants
                                        ) = subsense_data
                                        definitions[subsense_id] = {
                                            "lemma": format_lemma(text),
                                            "pos": pos,
                                            "definition": definition,
                                            "texts": texts + notes,
                                            "synonyms": synonyms,
                                            "variants": variants + sense_variants,
                                            "domains": domains,
                                            "source": "OX",
                                        }
    return definitions


def main():
    #with open(OXFORD_FILTERED_1, "r") as file:
    #    lemma_regions = file.read().splitlines()
    #    lemmas = [lemma_region.split("|")[0] for lemma_region in lemma_regions]

    lemmas = [ "stringed" ]
    print("Status:", "get sentence counts")
    sentence_counts = get_sense_sentence_counts(lemmas)
    print("Status:", "get sentence definitions")
    definitions = get_sense_definitions(lemmas)

    print("Status:", "filtering lemmas")
    sense_ids = definitions.keys()

    print("Has stringed", "m_en_gbus1003120.006" in sense_ids)
    print(definitions["m_en_gbus1003120.006"]["pos"])
    print(sentence_counts["m_en_gbus1003120.006"])
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

    #with open(OXFORD_FILTERED_2, "w+") as file:
    #    file.write(json.dumps(filtered_definitions, sort_keys=True, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
