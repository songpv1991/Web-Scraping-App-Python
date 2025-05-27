import sqlite3

class DatabaseManager:
    def __init__(self, db_name="odds.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS odds_drop (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                match TEXT,
                outcome TEXT,
                market TEXT,
                old REAL,
                new REAL,
                drop_percent TEXT,
                timestamp TEXT
            )
        ''')
        self.conn.commit()

    def insert_data(self, row):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO odds_drop (match, outcome, market, old, new, drop_percent, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', row)
        self.conn.commit()
