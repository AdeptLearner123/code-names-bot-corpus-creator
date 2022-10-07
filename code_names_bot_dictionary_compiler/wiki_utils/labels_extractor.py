from .wiki_utils import format_title

def get_title_label(title):
    title = title.replace("_", " ")
    if " (" not in title:
        return None
    return title.split(" (")[1][:-1] 


def extract_labels(variants, main_title, redirects):
    variants = set(variants)
    titles = [main_title] + redirects

    labels = []
    for title in titles:
        formatted_title = format_title(title)
        if formatted_title in variants:
            label = get_title_label(title)
            if label is not None:
                labels.append(label.lower())
    labels = list(set(labels))
    return labels