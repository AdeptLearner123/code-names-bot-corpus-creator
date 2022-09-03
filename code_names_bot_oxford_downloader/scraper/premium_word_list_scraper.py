import os

from unidecode import unidecode
from .scraper import scrape


WORD_OVERRIDES = {"°": "°"}

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
    word = word.replace("/", "{")  # Replace forward slash so file name is valid. Will reverse when getting URL. (sacrifice-someone/-on-the-altar-of)
    word = (
        unidecode(word).lower().replace(" ", "-").replace(",", "").replace("?", "%3F")
    )
    return word.replace(">", "\u2014").replace("<", "\u2013")


def get_targets(word_list_targets_dir):
    targets = []
    for file_name in os.listdir(word_list_targets_dir):
        letter = file_name.split(".")[0]
        with open(
            os.path.join(word_list_targets_dir, file_name), "r"
        ) as file:
            targets += list(
                map(
                    lambda first_word: f"{letter}|{format_word(first_word)}",
                    file.read().splitlines(),
                )
            )
    return targets


def scrape_premium(word_list_targets_dir, word_lists_dir, dictionary_name):
    print(format_word("Wouldn't you like to know?"))
    targets = get_targets(word_list_targets_dir)

    get_url = lambda item: f"https://premium-oxforddictionaries-com.offcampus.lib.washington.edu/us/browse/{dictionary_name}/{item.split('|')[0]}/{item.split('|')[1].replace('{', '/')}/"

    scrape(
        get_url,
        targets,
        extract,
        word_lists_dir,
        headers={
            "User-Agent": "Mozilla/6.0",
            "Cookie": "_ga=GA1.2.1761768241.1655574857; _ga_3T65WK0BM8=GS1.1.1661471019.7.0.1661471019.0.0.0; _ga_JLHM9WH4JV=GS1.1.1661471019.7.0.1661471019.0.0.0; nmstat=10857d25-4bfe-6f03-1dc1-5298ad5578ca; _mkto_trk=id:131-AQO-225&token:_mch-washington.edu-1656568436075-85816; _ga_57P4HTBKTG=GS1.1.1658767967.2.0.1658767967.0; ezproxyuwlib=VssrCGwWlIU7USt; localisation=US; JSESSIONID=073322D30426BD41781DCDF46732DBD4; SaneID=oi6OAmvT8jP-dQNDAmp; cookieLaw=true; XSRF-TOKEN=76e016fc-872c-4865-8702-19fe67d50859",
        },
    )