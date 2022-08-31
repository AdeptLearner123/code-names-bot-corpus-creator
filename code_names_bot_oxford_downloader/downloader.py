import os

import os
from config import TARGET_LEMMA_LISTS
from .oxford_definitions import OxfordDefinitions


def main():
    oxford_definitions = OxfordDefinitions()
    cached = oxford_definitions.get_all_cached()
    print("Cached", len(cached))

    targets = set()
    for file_name in os.listdir(TARGET_LEMMA_LISTS):
        with open(os.path.join(TARGET_LEMMA_LISTS, file_name), "r") as file:
            targets.update(file.read().splitlines())
    filtered_targets = targets - set(cached)

    print("All targets: ", len(targets))
    print("Filtered targets: ", len(filtered_targets))



if __name__ == "__main__":
    main()
