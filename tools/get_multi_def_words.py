from code_names_bot_dictionary_compiler.download.caches import OxfordDefinitionsCache
from code_names_bot_dictionary_compiler.oxford_utils.sense_iterator import iterate_senses

def main():
    definitions_cache = OxfordDefinitionsCache()
    for lexical_entry, _, sense, _ in iterate_senses(definitions_cache):
        if len(sense["definitions"]) > 1:
            print(lexical_entry["text"], sense["id"])
        if "crossReferences" in sense:
            cross_references = [ cf for cf in sense["crossReferences"] if cf["type"] == "another term for" ]
            if len(cross_references) > 1:
                print("Multiple cross reference", lexical_entry["text"], sense["id"])

if __name__ == "__main__":
    main()