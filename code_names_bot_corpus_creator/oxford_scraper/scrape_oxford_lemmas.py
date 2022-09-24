from config import (SCRAPED_INDICES_US_DIR, SCRAPED_INDICES_WORLD_DIR,
                    SCRAPED_LEMMAS_US_DIR, SCRAPED_LEMMAS_WORLD_DIR)

from .indices_scraper import scrape_indices
from .lemmas_scraper import scrape_lemmas


def main():
    scrape_indices(SCRAPED_INDICES_US_DIR, "american_english")
    scrape_indices(SCRAPED_INDICES_WORLD_DIR, "english")

    scrape_lemmas(
        SCRAPED_INDICES_US_DIR,
        SCRAPED_LEMMAS_US_DIR,
        "american_english",
    )

    scrape_lemmas(
        SCRAPED_INDICES_WORLD_DIR,
        SCRAPED_LEMMAS_WORLD_DIR,
        "english",
    )


if __name__ == "__main__":
    main()
