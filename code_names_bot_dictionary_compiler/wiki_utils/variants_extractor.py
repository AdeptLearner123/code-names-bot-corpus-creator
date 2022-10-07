from .wiki_utils import format_title
import spacy

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("merge_entities")
tokenizer = nlp.tokenizer

EXCLUDE_ENT_TYPES = set(["CARDINAL", "DATE", "MONEY", "ORDINAL", "PERCENT", "QUANTITY", "TIME"])


def get_children_by_dep(token, dep_types):
    return [ child for child in token.children if child.dep_ in dep_types ]


def get_child_entities(token):
    ents = [ child.text for child in token.children if len(child.ent_type_) > 0 and child.ent_type_ not in EXCLUDE_ENT_TYPES ]
    for child in token.children:
        ents += get_child_entities(child)
    return ents


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


def get_sentence_variants(sentence):
    nsubj = get_children_by_dep(sentence.root, "nsubj")[0]
    acl_children = get_children_by_dep(nsubj, ["acl", "appos"])
    ents = [ nsubj.text ]
    for child in acl_children:
        ents += get_child_entities(child)
    return ents


def get_tokens(str):
    return set([ token.text for token in tokenizer(str) ])


def extract_variants(title, summary, redirects):
    variants = list()
    variants.append(format_title(title))

    doc = nlp(summary)
    doc = merge_compounds(doc)
    sentence = list(doc.sents)[0]
    variants += get_sentence_variants(sentence)

    variants_tokenized = [ get_tokens(variant) for variant in variants ]
    redirect_variants = []
    for redirect in redirects:
        redirect = format_title(redirect)
        redirect_tokens = get_tokens(redirect)
        
        if any(redirect_tokens.issubset(variant_tokens) for variant_tokens in variants_tokenized):
            redirect_variants.append(redirect)
    
    variants += redirect_variants
    variants = list(set(variants))
    return variants