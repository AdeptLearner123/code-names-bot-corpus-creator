import json
import sys

from code_names_bot_corpus_creator.caches.oxford_cache import OxfordCache


def main():
    query = sys.argv[1]
    oxford_cache = OxfordCache()
    result = oxford_cache.get_cached_word_result(query)

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
