import json
import sqlite3

from config import OXFORD_CACHE


class OxfordCache:
    def __init__(self):
        self.con = sqlite3.connect(OXFORD_CACHE)
        self.cur = self.con.cursor()
        self.setup()

    def setup(self):
        self.cur.execute(
            """
                CREATE TABLE IF NOT EXISTS oxford_cache (
                    query TEXT NOT NULL UNIQUE,
                    words_result TEXT
                );
            """
        )
        self.cur.execute(
            """
                CREATE INDEX IF NOT EXISTS query_index ON oxford_cache (query);
            """
        )

    def insert_query(self, query):
        self.cur.execute("INSERT INTO oxford_cache (query) VALUES (?)", [query])

    def get_cached_word_result(self, query):
        self.cur.execute(
            "SELECT words_result FROM oxford_cache WHERE query=? LIMIT 1", [query]
        )
        return self.cur.fetchone()[0]

    def cache_words_result(self, query, words_result):
        self.cur.execute(
            "UPDATE oxford_cache SET words_result=? WHERE query=?;",
            [words_result, query],
        )

    def get_all_cached(self):
        self.cur.execute(
            "SELECT query FROM oxford_cache WHERE words_result IS NOT NULL;"
        )
        rows = self.cur.fetchall()
        return [row[0] for row in rows]

    def commit(self):
        self.con.commit()
