from .cache import Cache
from config import OXFORD_CACHE


class OxfordCache(Cache):
    def __init__(self):
        super().__init__(OXFORD_CACHE, False)
