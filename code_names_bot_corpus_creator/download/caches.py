from .cache import Cache
from config import OXFORD_CACHE, WIKI_PAGE_VIEWS_CACHE


class OxfordCache(Cache):
    def __init__(self):
        super().__init__(OXFORD_CACHE, False)


class WikiPageViewCache(Cache):
    def __init__(self):
        super().__init__(WIKI_PAGE_VIEWS_CACHE, True)