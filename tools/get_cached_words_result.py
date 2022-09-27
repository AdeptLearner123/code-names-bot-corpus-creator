import json
import sys

from code_names_bot_corpus_creator.download.caches import OxfordDefinitionsCache


def main():
    query = sys.argv[1]
    oxford_cache = OxfordDefinitionsCache()
    result = oxford_cache.get_cached_value(query)

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
