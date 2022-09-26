import sqlite3

from config import WIKI_PAGE_VIEWS_CACHE


class WikiPageViewsCache:
    def __init__(self):
        self.con = sqlite3.connect(WIKI_PAGE_VIEWS_CACHE)
        self.cur = self.con.cursor()
        self.setup()

    def setup(self):
        self.cur.execute(
            """
                CREATE TABLE IF NOT EXISTS wiki_page_views_cache (
                    page_id INT NOT NULL UNIQUE,
                    title TEXT NOT NULL UNIQUE,
                    page_views INT NOT NULL
                );
            """
        )
        self.cur.execute(
            """
                CREATE INDEX IF NOT EXISTS title_index ON wiki_page_views_cache (title);
            """
        )

    def get_cached_page_views(self, title):
        self.cur.execute(
            "SELECT page_views FROM wiki_page_views_cache WHERE title=? LIMIT 1",
            [title],
        )
        return self.cur.fetchone()[0]

    def cache_page_views(self, page_id, title, page_views):
        self.cur.execute(
            "INSERT INTO wiki_page_views_cache (page_id, title, page_views) VALUES (?, ?, ?);",
            [page_id, title, page_views],
        )

    def get_cached_titles(self):
        self.cur.execute("SELECT title FROM wiki_page_views_cache;")
        rows = self.cur.fetchall()
        return [row[0] for row in rows]

    def commit(self):
        self.con.commit()
