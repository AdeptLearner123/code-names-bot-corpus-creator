from code_names_bot_corpus_creator.download.caches import WikiPageViewCache
from config import WIKI_FILTERED_2, WIKI_FILTERED_3

PAGE_VIEW_THRESHOLD = 80000


def main():
    with open(WIKI_FILTERED_2) as file:
        lines = file.read().splitlines()
        titles = [line.split("\t")[1] for line in lines]
        title_to_line = {title: line for title, line in zip(titles, lines)}

    cache = WikiPageViewCache()
    title_to_views = cache.get_key_to_value()

    titles = filter(lambda title: title_to_views[title] > PAGE_VIEW_THRESHOLD, titles)
    lines = [title_to_line[title] for title in titles]

    with open(WIKI_FILTERED_3, "w+") as file:
        file.write("\n".join(lines))


if __name__ == "__main__":
    main()
