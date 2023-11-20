import sqlite3


class DataBaseSqlite:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def create_table(self):
        with self.connection:
            return self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users_dino(
                id INTEGER NOT NULL PRIMARY KEY, 
                first_name TEXT(70),
                last_name TEXT(80),
                nickname TEXT(60),
                active INTEGER NOT NULL
                );
                """
            )

    def add_new_user(self, id, first_name, last_name, nickname):
        with self.connection:
            try:
                sql = "INSERT INTO users_dino(id, first_name, last_name, nickname) " \
                      "VALUES(?, ?, ?, ?);"
                return self.cursor.execute(sql, (id, first_name, last_name, nickname,))
            except sqlite3.IntegrityError:
                pass

    def set_users_active(self, id, active):
        with self.connection:
            sql = "UPDATE users_dino SET active=? WHERE id=?;"
            return self.cursor.execute(sql, (active, id,))

    def get_users(self):
        with self.connection:
            sql = "SELECT id, active FROM users_dino;"
            return self.cursor.execute(sql).fetchall()




