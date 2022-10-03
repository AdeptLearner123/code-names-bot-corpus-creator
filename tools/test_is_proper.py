import sys

from code_names_bot_dictionary_compiler.utils.spacy_utils import is_proper


def main():
    print(is_proper(sys.argv[1]))


if __name__ == "__main__":
    main()
