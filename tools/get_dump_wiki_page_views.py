import os
import sys

from config import DUMP_WIKI_PAGE_VIEWS


def main():
    with open(DUMP_WIKI_PAGE_VIEWS, "r") as file:
        lines = file.read().splitlines()
        lines = [line.split(" ") for line in lines]
        page_views = {line[0]: int(line[1]) for line in lines}

    while True:
        title = input("Enter article title:")
        print(page_views[title])


if __name__ == "__main__":
    main()
