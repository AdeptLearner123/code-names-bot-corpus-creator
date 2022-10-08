import sys

import spacy
from spacy import displacy


def main():
    nlp = spacy.load("en_core_web_sm")
    # nlp.add_pipe("merge_entities")
    doc = nlp(sys.argv[1])

    displacy.serve(doc, style="dep", port=5001)


if __name__ == "__main__":
    main()
