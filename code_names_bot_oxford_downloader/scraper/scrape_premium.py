from config import PREMIUM_OXFORD_WORD_LIST_DIR_US, PREMIUM_OXFORD_WORD_LIST_DIR_WORLD, PREMIUM_OXFORD_WORD_LIST_TARGETS_DIR_US, PREMIUM_OXFORD_WORD_LIST_TARGETS_DIR_WORLD

from .premium_word_list_scraper import scrape_premium
from .premium_word_list_target_scraper import scrape_targets


def scrape_targets_us():
    scrape_targets(PREMIUM_OXFORD_WORD_LIST_TARGETS_DIR_US, "american_english")


def scrape_words_us():
    scrape_premium(PREMIUM_OXFORD_WORD_LIST_TARGETS_DIR_US, PREMIUM_OXFORD_WORD_LIST_DIR_US, "american_english")


def scrape_targets_world():
    scrape_targets(PREMIUM_OXFORD_WORD_LIST_TARGETS_DIR_WORLD, "english")


def scrape_words_world():
    scrape_premium(PREMIUM_OXFORD_WORD_LIST_TARGETS_DIR_WORLD, PREMIUM_OXFORD_WORD_LIST_DIR_WORLD, "english")