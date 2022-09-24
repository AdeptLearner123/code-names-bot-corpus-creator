Downloading Oxford lemmas
1. Scrape oxford premium for a list of lemmas ``poetry run scrape-oxford-lemmas``
    a. The result of the scraper are already included
    b. You will need to set the cookie on the scraper
2. Create a filtered list of lemmas to download ``poetry run create-filtered-lemmas-list``
3. Download Oxford lemma entries ``poetry run download-lemmas-entries``

Downloading Wikipedia page titles and ids
1. Download dump from https://dumps.wikimedia.org/enwiki/latest/
2. Download MySQL and read the dump into a database
