from .connect import get_connect
def create_table():
    sql = """
        CREATE TABLE IF NOT EXISTS users(
            id BIGSERIAL PRIMARY KEY,
            chat_id BIGINT NOT NULL UNIQUE,
            name VARCHAR(100) NOT NULL,
            user_name VARCHAR(100),
            phone VARCHAR(50),
            is_admin BOOL DEFAULT FALSE
    
        );
        CREATE TABLE IF NOT EXISTS books(
            id BIGSERIAL PRIMARY KEY,
            title VARCHAR(150) NOT NULL,
            description text,
            author VARCHAR(100) NOT NULL,
            genre VARCHAR(50),
            price BIGINT NOT NULL,
            quantity BIGINT NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS orders(
            id BIGSERIAL PRIMARY KEY,
            book_id BIGINT REFERENCES books(id),
            user_id BIGINT REFERENCES users(id),
            price BIGINT NOT NULL,
            quantity BIGINT NOT NULL DEFAULT 1,
            status VARCHAR(50) DEFAULT 'new',
            create_at timestamp DEFAULT now()
        );

"""
    with get_connect() as db:
        with db.cursor() as dbc:
            dbc.execute(sql)
        db.commit()
create_table()

def save_user(chat_id,fullname, phone, username=None):
    sql = """
    INSERT INTO users (chat_id, name, user_name, phone, is_admin)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (chat_id) DO NOTHING;
    """
    try:
        with get_connect() as db:
            with db.cursor() as dbc:
                dbc.execute(sql, (chat_id, fullname, phone, username))
    except:
        return None
    return True


def is_register_by_chat_id(chat_id: int) -> bool:
    try:
        sql = "SELECT * FROM users WHERE chat_id = %s;"

        with get_connect() as db:
            with db.cursor() as dbc:
                dbc.execute(sql, (chat_id,))
                return dbc.fetchone()
    except:
        return None


def find_books(kind, text):
    try:
        sql = "SELECT * FROM users WHERE chat_id = %s;"

        with get_connect() as db:
            with db.cursor() as dbc:
                if kind == "title":
                    dbc.execute("SELECT * FROM books WHERE title ilike '%%s%'",(text))
                elif kind == "genre":
                    dbc.execute("SELECT * FROM books WHERE genre ilike '%%s%'",(text))
                elif kind == "author":
                    dbc.execute("SELECT * FROM books WHERE author ilike '%%s%'",(text))
                else:
                    return None
                return dbc.fetchone()
            
    except:
        return None
