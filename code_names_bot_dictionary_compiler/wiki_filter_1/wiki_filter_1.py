from tqdm import tqdm

from code_names_bot_dictionary_compiler.wiki_utils.entity_classifier import is_entity
from config import DUMP_WIKI_PAGE_VIEWS, WIKI_PAGES, WIKI_FILTERED_1


PAGE_VIEW_THRESHOLD = 8000


def main():
    print("Status:", "Reading dump page views")
    with open(DUMP_WIKI_PAGE_VIEWS, "r") as file:
        lines = file.read().splitlines()
        lines = [line.split(" ") for line in lines]
        page_views = {line[0]: int(line[1]) for line in lines}

    print("Status:", "Reading wiki page titles")
    with open(WIKI_PAGES) as file:
        page_id_titles = file.read().splitlines()
        page_id_titles = map(
            lambda page_id_title: page_id_title.split("\t"), page_id_titles
        )

    print("Status:", "Filtering by dump page views")
    filtered_by_dump_page_views = filter(
        lambda page_id_title: page_id_title[1] in page_views
        and page_views[page_id_title[1]] > PAGE_VIEW_THRESHOLD,
        page_id_titles,
    )

    print("Status:", "Filtering for entities only")
    filtered_non_lists = filter(
        lambda page_id_title: is_entity(page_id_title[1]),
        tqdm(list(filtered_by_dump_page_views)),
    )

    print("Status:", "Dumping")
    filtered_page_id_titles = list(
        map(lambda page_id_title: "\t".join(page_id_title), filtered_non_lists)
    )

    with open(WIKI_FILTERED_1, "w+") as file:
        file.write("\n".join(filtered_page_id_titles))


if __name__ == "__main__":
    main()
