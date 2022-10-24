from tqdm import tqdm
import json

def sense_is_valid(sense_json):
    return "id" in sense_json and "definitions" in sense_json


def iterate_senses(definitions_cache, queries = None):
    query_to_result = definitions_cache.get_key_to_value()

    if queries is None:
        queries = tqdm(list(query_to_result.keys()))
    
    for query in queries:
        if query not in query_to_result:
            continue

        results_str = query_to_result[query]
        results = json.loads(results_str)
        for result in results["results"]:
            for lexical_entry in result["lexicalEntries"]:
                for entry in lexical_entry["entries"]:
                    if "senses" in entry:
                        for sense_idx, sense in enumerate(entry["senses"]):
                            if sense_is_valid(sense):
                                yield lexical_entry, entry, sense, (sense_idx, False)

                            if "subsenses" in sense:
                                for subsense_idx, subsense in enumerate(sense["subsenses"]):
                                    if sense_is_valid(subsense):
                                        yield lexical_entry, entry, subsense, (subsense_idx, True)