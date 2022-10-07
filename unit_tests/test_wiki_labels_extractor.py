import yaml

from code_names_bot_dictionary_compiler.wiki_utils.variants_extractor import extract_variants
from code_names_bot_dictionary_compiler.wiki_utils.labels_extractor import extract_labels
from code_names_bot_dictionary_compiler.wiki_utils.redirects_categories_parser import parse_redirects_categories
from code_names_bot_dictionary_compiler.download.caches import WikiRedirectsCategoriesCache, WikiSummariesCache
from config import EXPECTED_WIKI_LABELS

def main():
    redirects_categories_cache = WikiRedirectsCategoriesCache()
    summaries_cache = WikiSummariesCache()

    with open(EXPECTED_WIKI_LABELS, "r") as file:
        expected_wiki_labels = yaml.safe_load(file)
    
    for title in expected_wiki_labels:
        results_categories_result = redirects_categories_cache.get_cached_value(title)
        summary = summaries_cache.get_cached_value(title)

        redirects, _ = parse_redirects_categories(results_categories_result)
        variants = extract_variants(title, summary, redirects)

        labels = extract_labels(variants, title, redirects)

        for expected_label in expected_wiki_labels[title]:
            if expected_label not in labels:
                print("Expected", title, "to have label label", expected_label)

if __name__ == "__main__":
    main()