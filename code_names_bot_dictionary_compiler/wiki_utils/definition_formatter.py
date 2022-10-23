from code_names_bot_dictionary_compiler.utils.spacy_utils import get_auxilary, format_sentence

import spacy
nlp = spacy.load("en_core_web_sm")

def format_definition(definition):
    doc = nlp(definition.strip().replace("\n", " "))
    auxilary = get_auxilary(doc)

    if auxilary is None:
        print("Missing auxilary ", definition)
        return format_sentence(doc)
    
    span = doc[auxilary.i + 1:]
    return format_sentence(span)