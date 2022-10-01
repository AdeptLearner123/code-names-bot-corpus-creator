from config import WIKI_FILTERED_3, DICTIONARY_OUTPUT, OXFORD_FILTERED_2

def format_title(title):
    return title.split("_(")[0].replace("_", " ").lower()


def main():
    with open(WIKI_FILTERED_3) as file:
        lines = file.read().splitlines()
        titles = [line.split("\t")[1] for line in lines]
        title_to_line = {title: line for title, line in zip(titles, lines)}

    with open(OXFORD_FILTERED_2) as file:
        oxford_lemmas = file.read().splitlines()
    
    title_to_views = cache.get_key_to_value()

    titles = filter(lambda title: title_to_views[title] > PAGE_VIEW_THRESHOLD, titles)
    titles = filter(lambda title: title not in EXCLUDE_PAGES, titles)
    lines = [title_to_line[title] for title in titles]

    with open(WIKI_FILTERED_3, "w+") as file:
        file.write("\n".join(lines))


if __name__ == "__main__":
    main()
