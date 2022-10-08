import sys

from code_names_bot_dictionary_compiler.wiki_utils.redirects_categories_parser import (
    parse_redirects_categories,
)
from code_names_bot_dictionary_compiler.download.caches import (
    WikiRedirectsCategoriesCache,
)


def main():
    title = sys.argv[1]

    redirects_categories_cache = WikiRedirectsCategoriesCache()
    results_categories_result = redirects_categories_cache.get_cached_value(title)

    redirects, categories = parse_redirects_categories(results_categories_result)

    print(redirects)
    print(categories)


if __name__ == "__main__":
    main()
