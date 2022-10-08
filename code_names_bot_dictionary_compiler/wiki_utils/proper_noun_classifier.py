import spacy

nlp = spacy.load("en_core_web_sm", disable=["ner"])


def is_proper(summary):
    doc = nlp(summary)

    pos_list = [token.pos_ for token in list(doc.noun_chunks)[0]]
    return "PROPN" in pos_list
