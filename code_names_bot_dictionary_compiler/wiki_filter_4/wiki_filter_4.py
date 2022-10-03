from code_names_bot_dictionary_compiler.download.caches import (
    WikiSummariesCache,
    WikiPageViewCache,
)
from code_names_bot_dictionary_compiler.utils.spacy_utils import is_proper
from config import WIKI_FILTERED_3, WIKI_FILTERED_4

import yaml
from tqdm import tqdm


def format_title(title):
    return title.split("_(")[0].replace("_", " ").lower()


def main():
    with open(WIKI_FILTERED_3) as file:
        lines = file.read().splitlines()
        titles = [line.split("\t")[1] for line in lines]
        title_to_redirects = {
            title: line.split("\t")[2].split("|") for title, line in zip(titles, lines)
        }

    cache = WikiSummariesCache()
    title_to_summary = cache.get_key_to_value()

    title_to_views = WikiPageViewCache().get_key_to_value()

    definitions = dict()

    for title in tqdm(titles):
        if title not in title_to_summary:
            continue

        summary = title_to_summary[title]

        # Higher_Secondary_School_Certificate has empty extract
        if len(summary) == 0:
            continue

        try:
            pos = "proper" if is_proper(summary) else "noun"
        except:
            print("Failed", title, summary)
            break

        redirects = title_to_redirects[title]

        formatted_title = format_title(title)
        if pos == "noun":
            formatted_title = title.lower()
            redirects = list(set([redirect.lower() for redirect in redirects]))

        definitions[title] = {
            "text": formatted_title,
            "pos": pos,
            "definition": summary,
            "variants": redirects,
            "views": title_to_views[title],
        }

    with open(WIKI_FILTERED_4, "w+") as file:
        file.write(yaml.dump(definitions, sort_keys=True, default_flow_style=None))


if __name__ == "__main__":
    main()
