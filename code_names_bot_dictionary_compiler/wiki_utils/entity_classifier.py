from code_names_bot_dictionary_compiler.utils.spacy_utils import merge_compounds

from .wiki_utils import format_title

import spacy

nlp = spacy.load("en_core_web_sm", disable=["ner"])

def is_entity(title):
    doc = nlp(format_title(title))
    merge_compounds(doc)
    return len(doc) == 1