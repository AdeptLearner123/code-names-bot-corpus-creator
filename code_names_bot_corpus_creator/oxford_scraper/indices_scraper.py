from .scraper import scrape


def extract_targets(soup):
    output = []

    results = soup.find("ul", {"class": "browseResultList"})
    for child in results.findChildren("li"):
        link = child.select_one("a")
        span = link.find_all("span")[0]
        output.append(span.text)
    return output


def scrape_indices(indices_dir, dictionary_name):
    targets = [*"abcdefghijklmnopqrstuvwxyz"] + ["0-9"]

    get_url = (
        lambda letter: f"https://premium-oxforddictionaries-com.offcampus.lib.washington.edu/us/browse/{dictionary_name}/{letter}/"
    )

    scrape(
        get_url,
        targets,
        extract_targets,
        indices_dir,
        headers={
            "User-Agent": "Mozilla/6.0",
            "Cookie": "_ga=GA1.2.1761768241.1655574857; _ga_3T65WK0BM8=GS1.1.1661471019.7.0.1661471019.0.0.0; _ga_JLHM9WH4JV=GS1.1.1661471019.7.0.1661471019.0.0.0; nmstat=10857d25-4bfe-6f03-1dc1-5298ad5578ca; _mkto_trk=id:131-AQO-225&token:_mch-washington.edu-1656568436075-85816; _ga_57P4HTBKTG=GS1.1.1658767967.2.0.1658767967.0; ezproxyuwlib=HsfMJFVlkZKnhW5; localisation=US; JSESSIONID=676F28D29FD329586B5E9C88188B6AE4; SaneID=oi6OAmvT8jP-dQNDAmp; cookieLaw=true; XSRF-TOKEN=2731da63-288e-4c96-9b6c-218f3e45aed1",
        },
    )
