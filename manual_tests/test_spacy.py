import sys

import spacy
from spacy import displacy


def main():
    nlp = spacy.load("en_core_web_sm")
    # nlp.add_pipe("merge_entities")
    doc = nlp(sys.argv[1])

    style = "dep" if len(sys.argv) < 3 else sys.argv[2]
    displacy.serve(doc, style=style, port=5001)


if __name__ == "__main__":
    main()
