import sqlite3
from .connect import get_connect


def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER NOT NULL UNIQUE,
        name TEXT NOT NULL,
        user_name TEXT,
        phone TEXT,
        is_admin INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        author TEXT NOT NULL,
        genre TEXT,
        price INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        image TEXT 
    );

    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        user_id INTEGER,
        price INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        status TEXT DEFAULT 'new',
        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (book_id) REFERENCES books(id),
        FOREIGN KEY (user_id) REFERENCES users(chat_id)
    );
    """
    with get_connect() as db:
        db.executescript(sql)
        db.commit()

create_table()


def save_user(chat_id, fullname, phone, username=None, is_admin=0):
    sql = """
    INSERT OR IGNORE INTO users (chat_id, name, user_name, phone, is_admin)
    VALUES (?, ?, ?, ?, ?);
    """
    try:
        with get_connect() as db:
            # to'g'ri ketma-ketlik: chat_id, name, user_name, phone, is_admin
            db.execute(sql, (chat_id, fullname, username, phone, is_admin))
            db.commit()
        return True
    except Exception as e:
        print("❌ save_user xatolik:", e)
        return None



def is_register_by_chat_id(chat_id: int):
    try:
        sql = "SELECT * FROM users WHERE chat_id = ?;"
        with get_connect() as db:
            cur = db.execute(sql, (chat_id,))
            return cur.fetchone()
    except Exception as e:
        print("❌ is_register_by_chat_id xatolik:", e)
        return None


def find_books(kind: str, text: str):
    try:
        with get_connect() as db:
            if kind == "title":
                cur = db.execute("SELECT id, title, author, genre FROM books WHERE title LIKE ?;", (f"%{text}%",))
            elif kind == "genre":
                cur = db.execute("SELECT id, title, author, genre FROM books WHERE genre LIKE ?;", (f"%{text}%",))
            elif kind == "author":
                cur = db.execute("SELECT id, title, author, genre FROM books WHERE author LIKE ?;", (f"%{text}%",))
            else:
                return []

            return cur.fetchall()
    except Exception as e:
        print("❌ find_books xatolik:", e)
        return []


def find_by_books_id(book_id):
    try:
        with get_connect() as db:
            cur = db.execute("SELECT id, title, author, genre FROM books WHERE id = ?;", (book_id,))
            return cur.fetchone()
    except Exception as e:
        print("❌ find_by_books_id xatolik:", e)
        return None




def order_save_books(book_id, chat_id, quantity, price):
    try:
        with get_connect() as db:
            db.execute(
                "INSERT INTO orders (book_id, user_id, price, quantity) VALUES (?, ?, ?, ?);",
                (book_id, chat_id, price, quantity)
            )
            db.commit()
            return True
    except Exception as e:
        print("Xatolik:", e)
        return None