import spacy

nlp = spacy.load("en_core_web_sm", disable=["ner"])


def split_sentences(text):
    doc = nlp(text)
    return [ sentence.text for sentence in doc.sents]