import sys

from code_names_bot_dictionary_compiler.wiki_utils.labels_extractor import extract_labels
from code_names_bot_dictionary_compiler.wiki_utils.variants_extractor import extract_variants
from code_names_bot_dictionary_compiler.wiki_utils.redirects_categories_parser import parse_redirects_categories
from code_names_bot_dictionary_compiler.download.caches import WikiRedirectsCategoriesCache, WikiSummariesCache

def main():
    title = sys.argv[1]

    redirects_categories_cache = WikiRedirectsCategoriesCache()
    summaries_cache = WikiSummariesCache()
    results_categories_result = redirects_categories_cache.get_cached_value(title)
    summary = summaries_cache.get_cached_value(title)

    redirects, _ = parse_redirects_categories(results_categories_result)
    variants = extract_variants(title, summary, redirects)

    labels = extract_labels(variants, title, redirects)
    print(labels)


if __name__ == "__main__":
    main()