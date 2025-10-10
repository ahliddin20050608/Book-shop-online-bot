from .connect import get_connect

def is_admin_by_id(chat_id):
    with get_connect() as db:
        data = db.execute("SELECT*FROM users WHERE chat_id = ? and is_admin = 1", (chat_id,))
        

        return data.fetchone()
