from .connect import get_connect

def is_admin_by_id(chat_id):
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE chat_id = ? AND is_admin = 1", (chat_id,))
    result = cursor.fetchone()
    conn.close()
    return result


def save_book(title, description, author, genre, price, quantity, image_path):
    try:
        conn = get_connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO books (title, description, author, genre, price, quantity, image)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, description, author, genre, price, quantity, image_path))
        conn.commit()  
        conn.close()
        print("✅ Kitob muvaffaqiyatli saqlandi!")
    except Exception as err:
        print("❌ Kitob saqlashda xatolik:", err)


def get_orders(status):
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE status = ? ", (status,))
    result = cursor.fetchall()
    conn.close()
    return result



def get_user_by_id(user_id):
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result



def get_book_by_id(book_id):
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    result = cursor.fetchone()
    conn.close()
    return result


def change_status(status, order_id):
    with get_connect() as db:
        data = db.execute("Update orders set status = ? WHERE id = ?",(status,order_id))
        return data.fetchone()
    

def get_all_users():
      with get_connect() as db:
        data = db.execute("SELECT * FROM users")
        return data.fetchall()
      
def get_all_books():
      with get_connect() as db:
        data = db.execute("SELECT * FROM books")
        return data.fetchall()
      
def get_all_admin():
       with get_connect() as db:
        data = db.execute("SELECT * FROM users WHERE is_admin = 1")
        return data.fetchall()
       
def get_all_orders():
      with get_connect() as db:
        data = db.execute("SELECT * FROM orders")
        return data.fetchall()


    