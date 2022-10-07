import json


def parse_redirects_categories(result_str):
    results = json.loads(result_str)
    redirects = []
    categories = []

    for result in results:
        page_result = list(result["query"]["pages"].values())[0]
        if "redirects" in page_result:
            redirects += [
                redirect["title"]
                for redirect in page_result["redirects"]
            ]

        if "categories" in page_result:
            categories += [
                category["title"]
                for category in page_result["categories"]
            ]
    
    return redirects, categories