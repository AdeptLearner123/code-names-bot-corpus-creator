import sys

import json

from code_names_bot_dictionary_compiler.download.caches import WikiRedirectsCategoriesCache

def get_title_label(title):
    if " (" not in title:
        return None
    return title.split(" (")[1][:-1] 

def get_redirect_labels(results):
    labels = []
    for result in results:
        page_result = list(result["query"]["pages"].values())[0]

        if "redirects" in page_result:
            labels += [
                get_title_label(redirect["title"])
                for redirect in page_result["redirects"]
            ]

    return labels


def main():
    cache = WikiRedirectsCategoriesCache()
    title = sys.argv[1]
    results = cache.get_cached_value(title)

    results = json.loads(results)
    labels = get_redirect_labels(results)
    labels.append(get_title_label(title))

    labels = list(set(filter(lambda label: label is not None, labels)))

    print(labels)


if __name__ == "__main__":
    main()