from config import DUMP_WIKI_PAGE_VIEWS, WIKI_PAGES, DUMP_PAGE_VIEW_FILTERED


PAGE_VIEW_THRESHOLD = 8000


def main():
    with open(DUMP_WIKI_PAGE_VIEWS, "r") as file:
        lines = file.read().splitlines()
        lines = [line.split(" ") for line in lines]
        page_views = {line[0]: int(line[1]) for line in lines}

    with open(WIKI_PAGES) as file:
        page_id_titles = file.read().splitlines()
        page_id_titles = map(
            lambda page_id_title: page_id_title.split("\t"), page_id_titles
        )
        page_id_titles = map(
            lambda page_id_title: (page_id_title[0], page_id_title[1]), page_id_titles
        )

    filtered_by_dump_page_views = filter(
        lambda _, title: title in page_views
        and page_views[title] > PAGE_VIEW_THRESHOLD,
        page_id_titles,
    )

    filtered_non_lists = filter(
        lambda _, title: not title.startswith("List_of_"), filtered_by_dump_page_views
    )

    filtered_page_id_titles = list(
        map(lambda page_id_title: "\t".join(page_id_title), filtered_non_lists)
    )

    with open(DUMP_PAGE_VIEW_FILTERED, "w+") as file:
        file.write("\n".join(filtered_page_id_titles))


if __name__ == "__main__":
    main()
