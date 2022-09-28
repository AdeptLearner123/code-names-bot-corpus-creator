import sqlite3


class Cache:
    def __init__(self, path, value_is_int=False):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
        self.setup(value_is_int)

    def setup(self, value_is_int):
        self.cur.execute(
            f"""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT NOT NULL UNIQUE,
                    value { "INT" if value_is_int else "TEXT" } NOT NULL
                );
            """
        )
        self.cur.execute(
            """
                CREATE INDEX IF NOT EXISTS key_index ON cache (key);
            """
        )

    def get_cached_value(self, key):
        self.cur.execute(
            "SELECT value FROM cache WHERE key=? LIMIT 1",
            [key],
        )
        return self.cur.fetchone()[0]

    def cache_value(self, key, value):
        self.cur.execute(
            "INSERT INTO cache (key, value) VALUES (?, ?);",
            [key, value],
        )

    def get_cached_keys(self):
        self.cur.execute("SELECT key FROM cache;")
        rows = self.cur.fetchall()
        return [row[0] for row in rows]

    def get_key_to_value(self):
        self.cur.execute("SELECT key, value FROM cache;")
        rows = self.cur.fetchall()
        return { row[0]: row[1] for row in rows }

    def delete_key(self, key):
        self.cur.execute("DELETE FROM cache WHERE key=?", [key])

    def commit(self):
        self.con.commit()
