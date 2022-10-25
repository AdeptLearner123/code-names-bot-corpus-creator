from code_names_bot_dictionary_compiler.download.caches import OxfordDefinitionsCache
from code_names_bot_dictionary_compiler.oxford_utils.sense_iterator import iterate_senses

def main():
    definitions_cache = OxfordDefinitionsCache()
    for lexical_entry, _, _, _ in iterate_senses(definitions_cache):
        if "derivatives" not in lexical_entry:
            continue

        lemma = lexical_entry["text"]
        derivatives = [ derivative["text"] for derivative in lexical_entry["derivatives"] ]
        print(lemma, derivatives)

if __name__ == "__main__":
    main()