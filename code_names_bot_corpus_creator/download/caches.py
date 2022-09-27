from .cache import Cache
from config import (
    OXFORD_DEFINITIONS_CACHE,
    OXFORD_SENTENCES_CACHE,
    WIKI_PAGE_VIEWS_CACHE,
)


class OxfordDefinitionsCache(Cache):
    def __init__(self):
        super().__init__(OXFORD_DEFINITIONS_CACHE, False)


class WikiPageViewCache(Cache):
    def __init__(self):
        super().__init__(WIKI_PAGE_VIEWS_CACHE, True)


class OxfordSentencesCache(Cache):
    def __init__(self):
        super().__init__(OXFORD_SENTENCES_CACHE, False)
