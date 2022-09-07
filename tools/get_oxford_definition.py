import json
import sys

from code_names_bot_oxford_downloader.oxford_definitions import OxfordDefinitions


def main():
    term = sys.argv[1]
    oxford_definitions = OxfordDefinitions()
    result, is_cached = oxford_definitions.get_words_result(term)
    
    if is_cached:
        print(" ----  From Cache  ---- ")
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
