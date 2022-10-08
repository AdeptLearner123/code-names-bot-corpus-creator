import spacy

nlp = spacy.load("en_core_web_sm", disable=["ner"])


def split_sentences(text):
    doc = nlp(text)
    return [ sentence.text for sentence in doc.sents]


def merge_compounds(doc):
    with doc.retokenize() as retokenizer:
        begin = None
        for token in doc:
            if token.tag_.startswith("NN") and begin == None:
                begin = token
            elif not token.tag_.startswith("NN") and token.text != "\u2013" and begin != None:
                retokenizer.merge(doc[begin.i:token.i])
                begin = None
    return doc
