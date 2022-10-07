import yaml

from code_names_bot_dictionary_compiler.wiki_utils.entity_classifier import is_entity

from config import EXPECTED_WIKI_ENTITIES

def main():
    with open(EXPECTED_WIKI_ENTITIES, "r") as file:
        expected_wiki_entities = yaml.safe_load(file)
    
    for title in expected_wiki_entities["Contains"]:
        if not is_entity(title):
            print("Expected ",  title, "to be entity")

    for title in expected_wiki_entities["Excludes"]:
        if is_entity(title):
            print("Expected ", title, " to not be entity")

if __name__ == "__main__":
    main()