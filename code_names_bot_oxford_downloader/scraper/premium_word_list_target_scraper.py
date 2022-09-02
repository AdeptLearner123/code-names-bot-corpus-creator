from config import PREMIUM_OXFORD_WORD_LIST_TARGETS_DIR

from .scraper import scrape

GET_URL = (
    lambda letter: f"https://premium-oxforddictionaries-com.offcampus.lib.washington.edu/us/browse/american_english/{letter}/"
)


def extract_targets(soup):
    output = []

    results = soup.find("ul", {"class": "browseResultList"})
    for child in results.findChildren("li"):
        link = child.select_one("a")
        span = link.find_all("span")[0]
        output.append(span.text)
    print("Output", len(output))
    return output


def main():
    targets = [*"abcdefghijklmnopqrstuvwxyz"] + ["0-9"]

    scrape(
        GET_URL,
        targets,
        extract_targets,
        PREMIUM_OXFORD_WORD_LIST_TARGETS_DIR,
        headers={
            "User-Agent": "Mozilla/6.0",
            "Cookie": "_ga=GA1.2.1761768241.1655574857; _ga_3T65WK0BM8=GS1.1.1661471019.7.0.1661471019.0.0.0; _ga_JLHM9WH4JV=GS1.1.1661471019.7.0.1661471019.0.0.0; nmstat=10857d25-4bfe-6f03-1dc1-5298ad5578ca; _mkto_trk=id:131-AQO-225&token:_mch-washington.edu-1656568436075-85816; _ga_57P4HTBKTG=GS1.1.1658767967.2.0.1658767967.0; ezproxyuwlib=jacs00pTiEcwmVF; _gid=GA1.2.1888116142.1662056817; localisation=US; JSESSIONID=F2BD42E4ADBF590C0831808540C8FB8E; SaneID=oi6OAmvT8jP-dQNDAmp; cookieLaw=true; XSRF-TOKEN=b74d8174-4ec7-4b07-bc66-15491c04ed30",
        },
    )


if __name__ == "__main__":
    main()
