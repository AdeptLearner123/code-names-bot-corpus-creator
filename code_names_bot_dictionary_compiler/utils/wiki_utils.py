def get_title_label(title):
    title = title.replace("_", " ")
    if " (" not in title:
        return None
    return title.split(" (")[1][:-1] 


def get_labels(titles):
    labels = [ get_title_label(title) for title in titles ]
    labels = list(set(filter(lambda label: label is not None, labels)))
    return labels