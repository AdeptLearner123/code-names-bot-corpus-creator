import sys

import json

from code_names_bot_dictionary_compiler.download.caches import WikiRedirectsCategoriesCache
from code_names_bot_dictionary_compiler.wiki_utils.wiki_utils import get_labels

def get_title_label(title):
    if " (" not in title:
        return None
    return title.split(" (")[1][:-1] 

def get_redirects(results):
    redirects = []
    for result in results:
        page_result = list(result["query"]["pages"].values())[0]

        if "redirects" in page_result:
            redirects += [
                redirect["title"]
                for redirect in page_result["redirects"]
            ]

    return redirects


def main():
    cache = WikiRedirectsCategoriesCache()
    title = sys.argv[1]
    results = cache.get_cached_value(title)
    results = json.loads(results)

    redirects = get_redirects(results)
    labels = get_labels(redirects + [title])
    print(labels)


if __name__ == "__main__":
    main()