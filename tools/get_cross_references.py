from code_names_bot_dictionary_compiler.download.caches import OxfordDefinitionsCache
from code_names_bot_dictionary_compiler.oxford_utils.cross_references import get_cross_references

def main():
    definitions_cache = OxfordDefinitionsCache()
    for reference_text, lemma, _ in get_cross_references(definitions_cache):
        print(reference_text, lemma)
    
if __name__ == "__main__":
    main()