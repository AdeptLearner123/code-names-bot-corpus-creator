import os

from unidecode import unidecode

from .scraper import scrape

LEMMA_OVERRIDES = {"°": "°"}


def extract(soup):
    output = []

    results = soup.find_all("ul", {"class": "browseResultList"})[1]
    for child in results.findChildren("li"):
        link = child.select_one("a")
        span = link.select_one("span")
        output.append(span.text)
    return output


def format_lemma(lemma):
    if lemma in LEMMA_OVERRIDES:
        return LEMMA_OVERRIDES[lemma]

    lemma = lemma.replace("\u2013", "<")  # Preserve en dash
    lemma = lemma.replace("\u2014", ">")  # Preserve em dash
    lemma = lemma.replace(
        "/", "{"
    )  # Replace forward slash so file name is valid. Will reverse when getting URL. (sacrifice-someone/-on-the-altar-of)
    lemma = (
        unidecode(lemma).lower().replace(" ", "-").replace(",", "").replace("?", "%3F")
    )
    return lemma.replace(">", "\u2014").replace("<", "\u2013")


def get_indices(indices_dir):
    indices = []
    for file_name in os.listdir(indices_dir):
        letter = file_name.split(".")[0]
        with open(os.path.join(indices_dir, file_name), "r") as file:
            indices += list(
                map(
                    lambda first_word: f"{letter}|{format_lemma(first_word)}",
                    file.read().splitlines(),
                )
            )
    return indices


def scrape_lemmas(indices_dir, lemmas_dir, dictionary_name):
    indices = get_indices(indices_dir)

    get_url = (
        lambda item: f"https://premium-oxforddictionaries-com.offcampus.lib.washington.edu/us/browse/{dictionary_name}/{item.split('|')[0]}/{item.split('|')[1].replace('{', '/')}/"
    )

    scrape(
        get_url,
        indices,
        extract,
        lemmas_dir,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0",  # "Mozilla/6.0",
            "Cookie": "_ga=GA1.2.1761768241.1655574857; _ga_3T65WK0BM8=GS1.1.1661471019.7.0.1661471019.0.0.0; _ga_JLHM9WH4JV=GS1.1.1661471019.7.0.1661471019.0.0.0; nmstat=10857d25-4bfe-6f03-1dc1-5298ad5578ca; _mkto_trk=id:131-AQO-225&token:_mch-washington.edu-1656568436075-85816; _ga_57P4HTBKTG=GS1.1.1658767967.2.0.1658767967.0; ezproxyuwlib=9fYmmapQwwaZpYD; localisation=US; JSESSIONID=24ED3A257E3F2C6290293A71384EF17F; SaneID=oi6OAmvT8jP-dQNDAmp; cookieLaw=true; _gid=GA1.2.156572230.1662243616; XSRF-TOKEN=c52caecd-a813-4414-8f1e-109a7abe9ab6",
        },
    )
