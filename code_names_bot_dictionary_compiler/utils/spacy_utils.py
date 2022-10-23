import spacy

nlp = spacy.load("en_core_web_sm", disable=["ner"])


def split_sentences(text):
    doc = nlp(text)
    return [sentence.text for sentence in doc.sents]


def merge_compounds(doc):
    with doc.retokenize() as retokenizer:
        begin = None
        for token in doc:
            if token.tag_.startswith("NN") and begin == None:
                begin = token
            elif (
                not token.tag_.startswith("NN")
                and token.text != "\u2013"
                and begin != None
            ):
                retokenizer.merge(doc[begin.i : token.i])
                begin = None
    return doc


def get_children_by_dep(token, dep_types):
    return [child for child in token.children if child.dep_ in dep_types]


def get_auxilary(sentence):
    for token in sentence:
        if token.pos_ == "AUX":
            return token
    return None


def format_sentence(sentence):
    sentence_text = sentence.text
    if sentence[0].pos_ != "PROPN":
        sentence_text = sentence_text[0].lower() + sentence_text[1:]
    if sentence_text[-1] == ".":
        sentence_text = sentence_text[:-1]
    return sentence_text


def format_sentence_text(sentence_text):
    sentence = nlp(sentence_text)
    return format_sentence(sentence)