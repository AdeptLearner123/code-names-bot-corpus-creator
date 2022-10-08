import yaml

from code_names_bot_dictionary_compiler.wiki_utils.variants_extractor import (
    extract_variants,
)
from code_names_bot_dictionary_compiler.wiki_utils.redirects_categories_parser import (
    parse_redirects_categories,
)
from code_names_bot_dictionary_compiler.download.caches import (
    WikiRedirectsCategoriesCache,
    WikiSummariesCache,
)
from config import EXPECTED_WIKI_VARIANTS


def main():
    redirects_categories_cache = WikiRedirectsCategoriesCache()
    summaries_cache = WikiSummariesCache()

    with open(EXPECTED_WIKI_VARIANTS, "r") as file:
        expected_wiki_variants = yaml.safe_load(file)

    for title in expected_wiki_variants:
        results_categories_result = redirects_categories_cache.get_cached_value(title)
        summary = summaries_cache.get_cached_value(title)

        redirects, _ = parse_redirects_categories(results_categories_result)
        variants = extract_variants(title, summary, redirects)

        contains_variants = (
            expected_wiki_variants[title]["Contains"]
            if "Contains" in expected_wiki_variants[title]
            else []
        )
        excludes_variants = (
            expected_wiki_variants[title]["Excludes"]
            if "Excludes" in expected_wiki_variants[title]
            else []
        )
        for contains_variant in contains_variants:
            if contains_variant not in variants:
                print("Expected ", title, "to have variant", contains_variant)

        for excludes_variant in excludes_variants:
            if excludes_variant in variants:
                print("Expected ", title, "to exclude variant", excludes_variant)


if __name__ == "__main__":
    main()
