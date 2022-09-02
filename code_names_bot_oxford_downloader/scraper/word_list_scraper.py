from config import OXFORD_WORD_LIST_DIR

from .scraper import scrape

GET_URL = (
    lambda page_id: f"https://www.oxfordreference.com/view/10.1093/acref/9780199571123.001.0001/acref-9780199571123?btog=chap&hide=true&pageSize=20&skipEditions=true&sort=titlesort&source=%2F10.1093%2Facref%2F9780199571123.001.0001%2Facref-9780199571123&page={page_id}"
)
TOTAL_PAGES = 5356


def extract_terms(soup):
    output = []
    items = soup.select(".itemTitle")
    for item in items:
        word = item.a.find(text=True, recursive=False)
        output.append(word.strip())
    return output


def main():
    target_ids = range(1, TOTAL_PAGES + 1)
    target_ids = list(map(lambda target_id: str(target_id), target_ids))
    scrape(GET_URL, target_ids, extract_terms, OXFORD_WORD_LIST_DIR, headers={"User-Agent": "Mozilla/6.0"})


if __name__ == "__main__":
    main()
