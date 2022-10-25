from .sense_iterator import iterate_senses

def get_cross_references(definitions_cache):
    cross_references = []
    for lexical_entry, _, sense, _ in iterate_senses(definitions_cache, check_has_def=False):
        if "definitions" in sense:
            continue
        if "crossReferences" not in sense:
            continue
        
        lemma = lexical_entry["text"]

        for cf in sense["crossReferences"]:
            if cf["type"] == "another term for":
                reference_text = cf["text"]
                cross_references.append((reference_text, lemma, sense))
    
    return cross_references