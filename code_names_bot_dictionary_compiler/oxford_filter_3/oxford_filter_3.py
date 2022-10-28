from code_names_bot_dictionary_compiler.download.caches import OxfordDefinitionsCache, OxfordSentencesCache
from code_names_bot_dictionary_compiler.oxford_utils.sense_iterator import iterate_senses
from code_names_bot_dictionary_compiler.oxford_utils.cross_references import get_cross_references
from config import OXFORD_FILTERED_2, OXFORD_FILTERED_3

import json
from collections import defaultdict

def get_sense_sentence_counts():
    sentences_cache = OxfordSentencesCache()
    query_to_result = sentences_cache.get_key_to_value()
    sentence_counts = defaultdict(lambda: 0)

    for results_str in query_to_result.values():
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

        is_proper = "proper" in grammatical_features or (lexical_category == "noun" and lexical_entry["text"][0].isupper())
        sense_pos[sense_id] = "proper" if is_proper else lexical_category
    return sense_pos


def extract_sense_data(lemma, sense_json):
    synonyms, domains, variant_forms, classes = [], [], [], []

    if "domainClasses" in sense_json:
        domains = [domain_class["text"].replace("_", " ").lower() for domain_class in sense_json["domainClasses"]]

    if "semanticClasses" in sense_json:
        classes = [semantic_class["text"].replace("_", " ").lower() for semantic_class in sense_json["semanticClasses"]]

    if "synonyms" in sense_json:
        synonyms = [synonym["text"] for synonym in sense_json["synonyms"]]
        if lemma in synonyms:
            synonyms.remove(lemma)
    
    if "variantForms" in sense_json:
        variant_forms = [ variant_form["text"] for variant_form in sense_json["variantForms"] ]
    
    return synonyms, domains, variant_forms, classes


def get_entry_variants(entry):
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

    return variants


def get_derivatives(lexical_entry):
    if "derivatives" not in lexical_entry:
        return []
    
    return [ derivative["text"] for derivative in lexical_entry["derivatives"] ]


def enhance_sense(lexical_entry, entry, sense, meta, dictionary, sentence_counts, sense_pos):
    sense_id = sense["id"]
    if sense_id not in dictionary:
        return
    
    lemma = dictionary[sense_id]["lemma"]

    derivatives = get_derivatives(lexical_entry)

    variants = get_entry_variants(entry)

    synonyms, domains, sense_variants, classes = extract_sense_data(lemma, sense)

    variants = set(variants + sense_variants)
    if lemma in variants:
        variants.remove(lemma)
    variants = list(variants)

    sense_idx, is_subsense = meta

    dictionary[sense_id].update({
        "variants": variants,
        "derivatives": derivatives,
        "synonyms": synonyms,
        "domains": domains,
        "classes": classes,
        "pos": sense_pos[sense_id],
        "meta": {
            "sense_idx": sense_idx,
            "is_subsense": is_subsense,
            "sentence_count": sentence_counts[sense_id]
        }
    })


def enhance_with_cross_references(dictionary, definitions_cache):
    # "Second World War" is not listed as a variant form in the entry for "World War II"
    # but "World War II" is listed as a cross reference in the entry for "Second World War"
    lemma_to_senses = defaultdict(lambda: [])
    for sense_id, entry in dictionary.items():
        lemma = entry["lemma"]
        lemma_to_senses[lemma.lower()].append(sense_id)
    
    cross_references = get_cross_references(definitions_cache)
    for reference_text, lemma, sense in cross_references:
        reference_text = reference_text.lower()

        if reference_text not in lemma_to_senses:
            continue

        referenced_senses = lemma_to_senses[reference_text]
        if len(lemma_to_senses[reference_text]) == 1:
            referenced_sense = lemma_to_senses[reference_text][0]
            dictionary[referenced_sense]["variants"].append(lemma)
            continue
        
        candidate_senses = [ sense for sense in referenced_senses if lemma in dictionary[sense]["synonyms"]]
        if len(candidate_senses) == 1:
            dictionary[candidate_senses[0]]["variants"].append(lemma)


def main():
    with open(OXFORD_FILTERED_2, "r") as file:
        dictionary = json.loads(file.read())

    definitions_cache = OxfordDefinitionsCache()

    print("Status:", "Enhancing senses")
    sentence_counts = get_sense_sentence_counts()

    print("Status:", "Get sense pos")
    sense_pos = get_sense_pos(definitions_cache)

    for lexical_entry, entry, sense, meta in iterate_senses(definitions_cache):
        enhance_sense(lexical_entry, entry, sense, meta, dictionary, sentence_counts, sense_pos)

    print("Status:", "Enhancing with cross references")
    enhance_with_cross_references(dictionary, definitions_cache)

    with open(OXFORD_FILTERED_3, "w+") as file:
        file.write(json.dumps(dictionary, sort_keys=True, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()