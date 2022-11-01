from config import WIKI_FILTERED_3, OXFORD_FILTERED_3, WIKI_FILTERED_4

import json
from tqdm import tqdm

from code_names_bot_dictionary_compiler.wiki_utils.proper_noun_classifier import (
    is_proper,
)
from code_names_bot_dictionary_compiler.wiki_utils.wiki_utils import format_title
from code_names_bot_dictionary_compiler.wiki_utils.definition_formatter import format_definition
from code_names_bot_dictionary_compiler.utils.spacy_utils import split_sentences, format_sentence_text
from code_names_bot_dictionary_compiler.download.caches import WikiSummariesCache

TARGET_LABELS = set(["company", "brand", "franchise", "film"])


def main():
    print("Status:", "reading")
    with open(OXFORD_FILTERED_3, "r") as file:
        oxford_dictionary = json.loads(file.read())

    print("Status:", "getting Oxford variants")
    oxford_lemmas = []
    for lemma in oxford_dictionary:
        oxford_lemmas += [oxford_dictionary[lemma]["lemma"].lower()]
        oxford_lemmas += [
            variant.lower() for variant in oxford_dictionary[lemma]["variants"]
        ]
    oxford_lemmas = set(oxford_lemmas)

    print("Status:", "reading Wiki titles list")
    with open(WIKI_FILTERED_3) as file:
        lines = file.read().splitlines()
        titles = [line.split("\t")[1] for line in lines]
        variants_list = [line.split("\t")[2].split("|") for line in lines]
        labels_list = [line.split("\t")[3].split("|") for line in lines]
        title_to_variants = {
            title: variants for title, variants in zip(titles, variants_list)
        }
        title_to_labels = {title: labels for title, labels in zip(titles, labels_list)}

    print("Status:", "filtering Wiki articles")
    filtered_titles = []
    title_variants = dict()
    for title in tqdm(titles):
        variants = title_to_variants[title]
        labels = title_to_labels[title]

        title_variants[title] = variants

        if any(label in TARGET_LABELS for label in labels) or not any(
            variant.lower() in oxford_lemmas for variant in variants
        ):
            filtered_titles.append(title)

    title_to_summary = WikiSummariesCache().get_key_to_value()
    filtered_titles = list(
        filter(
            lambda title: title in title_to_summary
            and is_proper(title_to_summary[title]),
            tqdm(filtered_titles),
        )
    )

    print("Status:", "compiling wiki dict")
    wiki_dict = dict()
    for title in tqdm(filtered_titles):
        formatted_title = format_title(title)
        summary = title_to_summary[title].replace("\n", "").replace("\t", "").strip()
        sentences = split_sentences(summary)
        try:
            definition = format_definition(sentences[0])
        except:
            print("Failed for ", title)
            raise
        texts = [ format_sentence_text(text) for text in sentences[1:] ]
        variants = title_variants[title]
        variants.remove(formatted_title)
        wiki_dict[title] = {
            "lemma": formatted_title,
            "source": "WI",
            "pos": "proper",
            "definition": definition,
            "texts": texts,
            "variants": variants,
            "derivatives": [],
            "synonyms": [],
            "domains": [],
            "classes": [],
            "meta": {
                "is_primary": True
            }
        }

    print("Status:", "dumping")
    with open(WIKI_FILTERED_4, "w+") as file:
        file.write(json.dumps(wiki_dict, sort_keys=True, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
