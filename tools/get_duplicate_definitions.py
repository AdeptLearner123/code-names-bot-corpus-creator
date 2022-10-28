from code_names_bot_dictionary_compiler.download.caches import OxfordDefinitionsCache
from code_names_bot_dictionary_compiler.oxford_utils.sense_iterator import iterate_senses

from collections import defaultdict

def main():
    definitions_cache = OxfordDefinitionsCache()
    definition_senses = defaultdict(lambda: set())
    for _, _, sense, _ in iterate_senses(definitions_cache):
        sense_id = sense["id"]
        definition = sense["definitions"][0]
        definition_senses[definition].add(sense_id)
    
    for definition, senses in definition_senses.items():
        if len(senses) > 1:
            print(definition, senses)

if __name__ == "__main__":
    main()