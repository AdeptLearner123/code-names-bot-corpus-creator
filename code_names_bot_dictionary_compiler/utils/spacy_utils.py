import spacy

nlp = spacy.load("en_core_web_sm", disable=["ner"])


def split_sentences(text):
    doc = nlp(text)
    return [ sentence.text for sentence in doc.sents]


def merge_compounds(doc):
    with doc.retokenize() as retokenizer:
        begin = None
        for token in doc:
            if token.dep_ == "compound" and begin == None:
                begin = token.i
            elif token.dep_ != "compound" and begin != None:
                retokenizer.merge(doc[begin:token.i + 1])
                begin = None
    return doc
