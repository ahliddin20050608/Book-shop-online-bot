import sqlite3

def get_connect():
    conn = sqlite3.connect("books.db")
    conn.row_factory = sqlite3.Row  # <-- Shu juda muhim
    return conn
