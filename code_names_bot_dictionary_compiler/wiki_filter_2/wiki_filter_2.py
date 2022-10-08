from tqdm import tqdm

from code_names_bot_dictionary_compiler.download.caches import (
    WikiRedirectsCategoriesCache,
    WikiSummariesCache,
)
from code_names_bot_dictionary_compiler.wiki_utils.redirects_categories_parser import (
    parse_redirects_categories,
)
from code_names_bot_dictionary_compiler.wiki_utils.variants_extractor import (
    extract_variants,
)
from code_names_bot_dictionary_compiler.wiki_utils.labels_extractor import (
    extract_labels,
)
from config import WIKI_FILTERED_1, WIKI_FILTERED_2


UNWANTED_CATEGORIES = set(
    ["Category:All set index articles", "Category:All disambiguation pages"]
)


def main():
    with open(WIKI_FILTERED_1) as file:
        page_id_titles = file.read().splitlines()
        page_id_titles = list(
            map(lambda page_id_title: page_id_title.split("\t"), page_id_titles)
        )
        title_to_page_id = {
            page_id_title[1]: page_id_title[0] for page_id_title in page_id_titles
        }
        titles = [page_id_title[1] for page_id_title in page_id_titles]

    redirects_categories_cache = WikiRedirectsCategoriesCache()
    summaries_cache = WikiSummariesCache()

    title_to_redirects_categories = redirects_categories_cache.get_key_to_value()
    title_to_summary = summaries_cache.get_key_to_value()
    titles = list(
        filter(
            lambda title: title in title_to_redirects_categories
            and title in title_to_summary,
            titles,
        )
    )

    filtered_titles = []
    title_to_variants = {}
    title_to_labels = {}
    for title in tqdm(titles):
        redirects, categories = parse_redirects_categories(
            title_to_redirects_categories[title]
        )

        if any(category in UNWANTED_CATEGORIES for category in categories):
            continue

        summary = title_to_summary[title]
        try:
            variants = extract_variants(title, summary, redirects)
        except:
            print("Failed", title)
            break
        if any(len(variant.split(" ")) <= 2 for variant in variants):
            filtered_titles.append(title)
            title_to_variants[title] = variants
            title_to_labels[title] = extract_labels(variants, title, redirects)

    with open(WIKI_FILTERED_2, "w+") as file:
        lines = [
            f"{title_to_page_id[title]}\t{title}\t{'|'.join(title_to_variants[title])}\t{'|'.join(title_to_labels[title])}"
            for title in filtered_titles
        ]
        file.write("\n".join(lines))


if __name__ == "__main__":
    main()
