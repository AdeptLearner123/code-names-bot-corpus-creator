from .cache import Cache
from config import (
    OXFORD_DEFINITIONS_CACHE,
    OXFORD_SENTENCES_CACHE,
    WIKI_PAGE_VIEWS_CACHE,
    WIKI_REDIRECTS_CATEGORIES_CACHE,
    WIKI_SUMMARIES_CACHE,
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


class WikiRedirectsCategoriesCache(Cache):
    def __init__(self):
        super().__init__(WIKI_REDIRECTS_CATEGORIES_CACHE, False)


class WikiSummariesCache(Cache):
    def __init__(self):
        super().__inti__(WIKI_SUMMARIES_CACHE, False)