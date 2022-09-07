import json
import sys

from code_names_bot_oxford_downloader.oxford_definitions import OxfordDefinitions


def main():
    oxford_definitions = OxfordDefinitions()
    cached = oxford_definitions.get_all_cached()
    print(list(cached))


if __name__ == "__main__":
    main()
