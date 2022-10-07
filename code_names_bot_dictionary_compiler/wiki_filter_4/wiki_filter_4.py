from config import WIKI_FILTERED_3, OXFORD_FILTERED_2, WIKI_FILTERED_4

import yaml
from tqdm import tqdm

from code_names_bot_dictionary_compiler.wiki_utils.wiki_utils import get_labels
from code_names_bot_dictionary_compiler.utils.spacy_utils import is_proper, split_sentences
from code_names_bot_dictionary_compiler.download.caches import WikiSummariesCache

TARGET_LABELS = set(["company", "brand", "franchise", "film"])

def format_title(title):
    return title.replace("_", " ").split(" (")[0]


def get_variants(main_title, redirects):
    titles = [ title for title in redirects if ":" not in title ]
    titles = [ format_title(title) for title in redirects ]
    titles = [ title for title in titles if len(title) > 0 ]
    titles = set(titles)
    if main_title in titles:
        titles.remove(main_title)
    titles = filter(lambda title: title.isascii(), titles)
    return list(titles)


def main():
    print("Status:", "reading")
    with open(OXFORD_FILTERED_2, "r") as file:
        oxford_dictionary = yaml.safe_load(file)
    
    print("Status:", "getting Oxford variants")
    oxford_lemmas = []
    for lemma in oxford_dictionary:
        oxford_lemmas += [ oxford_dictionary[lemma]["lemma"].lower() ]
        oxford_lemmas += [ variant.lower() for variant in oxford_dictionary[lemma]["variants"] ]
    oxford_lemmas = set(oxford_lemmas)

    print("Status:", "reading Wiki titles list")
    with open(WIKI_FILTERED_3) as file:
        lines = file.read().splitlines()
        titles = [ line.split("\t")[1] for line in lines ]
        redirects = [ line.split("\t")[2].split("|") for line in lines ]
        title_to_redirects = { title: redirects for title, redirects in zip(titles, redirects) }

    print("Status:", "filtering Wiki articles")
    filtered_titles = []
    title_variants = dict()
    for title in tqdm(titles):
        redirects = title_to_redirects[title]
        labels = get_labels([title] + redirects)

        variants = get_variants(title, redirects)
        lemma_forms = variants + [title]

        title_variants[title] = variants

        if any(label in TARGET_LABELS for label in labels) or not any(lemma_form.lower() in oxford_lemmas for lemma_form in lemma_forms):
            filtered_titles.append(title)

    title_to_summary = WikiSummariesCache().get_key_to_value()
    filtered_titles = list(filter(lambda title: title in title_to_summary and is_proper(title_to_summary[title]), filtered_titles))

    print("Status:", "compiling wiki dict")
    wiki_dict = dict()
    for title in tqdm(filtered_titles):
        sentences = split_sentences(title_to_summary[title])
        definition = sentences[0]
        texts = sentences[1:]
        wiki_dict[title] = {
            "lemma": format_title(title),
            "definition": definition,
            "texts": texts,
            "variants": title_variants[title],
            "pos": "proper",
            "source": "WI"
        }

    print("Status:", "dumping")
    with open(WIKI_FILTERED_4, "w+") as file:
        yaml.dump(wiki_dict, file, sort_keys=True, allow_unicode=True)


if __name__ == "__main__":
    main()
