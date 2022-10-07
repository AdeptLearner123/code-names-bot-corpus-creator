def get_title_label(title):
    title = title.replace("_", " ")
    if " (" not in title:
        return None
    return title.split(" (")[1][:-1] 


def get_labels(titles):
    labels = [ get_title_label(title) for title in titles ]
    labels = list(set(filter(lambda label: label is not None, labels)))
    return labels

def format_title(title):
    return title.replace("_", " ").split(" (")[0]


def get_variants(main_title, redirects, extract):
    titles = [ title for title in redirects if ":" not in title ]
    titles = [ format_title(title) for title in redirects ]
    titles = [ title for title in titles if len(title) > 0 ]
    titles = set(titles)
    if main_title in titles:
        titles.remove(main_title)
    titles = filter(lambda title: title.isascii(), titles)
    return list(titles)