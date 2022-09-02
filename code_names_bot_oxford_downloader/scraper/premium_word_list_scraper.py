import os
from ast import literal_eval as make_tuple

from unidecode import unidecode

from config import (PREMIUM_OXFORD_WORD_LIST_DIR,
                    PREMIUM_OXFORD_WORD_LIST_TARGETS_DIR)

from .scraper import scrape

WORD_OVERRIDES = {"°": "°"}

GET_URL = (
    lambda item: f"https://premium-oxforddictionaries-com.offcampus.lib.washington.edu/us/browse/american_english/{item.split('|')[0]}/{item.split('|')[1]}/"
)
# GET_URL = lambda str: "Joke " + str


def extract(soup):
    output = []

    results = soup.find_all("ul", {"class": "browseResultList"})[1]
    for child in results.findChildren("li"):
        link = child.select_one("a")
        span = link.select_one("span")
        output.append(span.text)
    return output


def format_word(word):
    if word in WORD_OVERRIDES:
        return WORD_OVERRIDES[word]

    word = word.replace("\u2013", "<")  # Preserve en dash
    word = word.replace("\u2014", ">")  # Preserve em dash
    word = (
        unidecode(word).lower().replace(" ", "-").replace(",", "").replace("?", "%3F")
    )
    return word.replace(">", "\u2014").replace("<", "\u2013")


def get_targets():
    targets = []
    for file_name in os.listdir(PREMIUM_OXFORD_WORD_LIST_TARGETS_DIR):
        letter = file_name.split(".")[0]
        with open(
            os.path.join(PREMIUM_OXFORD_WORD_LIST_TARGETS_DIR, file_name), "r"
        ) as file:
            targets += list(
                map(
                    lambda first_word: f"{letter}|{format_word(first_word)}",
                    file.read().splitlines(),
                )
            )
    return targets


def main():
    print(format_word("Wouldn't you like to know?"))
    targets = get_targets()

    scrape(
        GET_URL,
        targets,
        extract,
        PREMIUM_OXFORD_WORD_LIST_DIR,
        headers={
            "User-Agent": "Mozilla/6.0",
            "Cookie": "_ga=GA1.2.1761768241.1655574857; _ga_3T65WK0BM8=GS1.1.1661471019.7.0.1661471019.0.0.0; _ga_JLHM9WH4JV=GS1.1.1661471019.7.0.1661471019.0.0.0; nmstat=10857d25-4bfe-6f03-1dc1-5298ad5578ca; _mkto_trk=id:131-AQO-225&token:_mch-washington.edu-1656568436075-85816; _ga_57P4HTBKTG=GS1.1.1658767967.2.0.1658767967.0; ezproxyuwlib=jacs00pTiEcwmVF; _gid=GA1.2.1888116142.1662056817; localisation=US; JSESSIONID=F2BD42E4ADBF590C0831808540C8FB8E; SaneID=oi6OAmvT8jP-dQNDAmp; cookieLaw=true; XSRF-TOKEN=b74d8174-4ec7-4b07-bc66-15491c04ed30",
        },
    )


if __name__ == "__main__":
    main()
