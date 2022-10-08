from .wiki_utils import format_title

import spacy

nlp = spacy.load("en_core_web_sm", disable=["ner"])
nlp.add_pipe("merge_noun_chunks")

def is_entity(title):
    doc = nlp(format_title(title))
    return len(doc) == 1