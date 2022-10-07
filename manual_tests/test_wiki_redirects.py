import yaml

from config import WIKI_FILTERED_4

def main():
    with open(WIKI_FILTERED_4, "r") as file:
        wiki_dict = yaml.safe_load(file)
    
    


if __name__ == "__main__":
    main()