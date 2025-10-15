import os

ADMIN_MAIN_TEXT = """
        Assalomu alaykum, Admin!
        Quyidagi menyudan tanlang:
        • Menu — mahsulotlarni boshqarish
        • Orders — buyurtmalarni ko‘rish
        • Dashboard — statistika"
    """

ADMIN_MENU = """
        📂 Admin Panel
        Quyidagi bo‘limlardan birini tanlang:
        ➕ Add — yangi narsa qo‘shish
        📋 All — barcha ma’lumotlarni ko‘rish
        🔙 Back — orqaga qaytish
    """

def convert_books_to_html(books):

    book_list = []
    for book in books:
        image_path = os.path.abspath(book[7])  # rasm manzili
        book_text = f"""
        <tr>
          <td>{book[0]}</td>
          <td>{book[1]}</td>
          <td>{book[2]}</td>
          <td>{book[3]}</td>
          <td>{book[4]}</td>
          <td>{book[5]} so‘m</td>
          <td>{book[6]}</td>
          <td><img src="{image_path}" alt="Not found" /></td>
        </tr>
        """
        book_list.append(book_text)

    book_list = "\n".join(book_list)
    html_text = f"""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Kitoblar ro‘yxati</title>
        <style>
            body {{
                font-family: "Poppins", sans-serif;
                background-color: #f8f9fc;
                margin: 0;
                padding: 0;
            }}
            .container {{
                width: 90%;
                margin: 40px auto;
                text-align: center;
            }}
            h1 {{
                color: #2d2dff;
                margin-bottom: 30px;
                font-size: 28px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background: #fff;
                border-radius: 10px;
                box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}
            thead tr {{
                background-color: #4a3aff;
                color: white;
            }}
            th, td {{
                padding: 15px;
                text-align: center;
                border-bottom: 1px solid #eaeaea;
            }}
            td img {{
                width: 60px;
                height: 60px;
                object-fit: cover;
                border-radius: 8px;
            }}
            tbody tr:hover {{
                background-color: #f1f3ff;
                transition: 0.3s;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📚 Kitoblar ro‘yxati</h1>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>NOMI</th>
                        <th>TAVSIF</th>
                        <th>MUALLIF</th>
                        <th>JANR</th>
                        <th>NARX</th>
                        <th>SAHIFA</th>
                        <th>RASM</th>
                    </tr>
                </thead>
                <tbody>
                    {book_list}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    return html_text





ORDERS_TEXT = """
📦 **Buyurtmalar bo‘limi**

Bu yerda foydalanuvchilarning barcha buyurtmalarini kuzatishingiz mumkin.

🟢 **New** — yangi tushgan buyurtmalar  
🟡 **In Progress** — tayyorlanayotgan yoki jo‘natilayotgan buyurtmalar  
🔵 **Finish** — yetkazilgan yoki yakunlangan buyurtmalar  
↩️ **Back** — admin panelga qaytish

Quyidagi menyudan kerakli bo‘limni tanlang ⤵️
"""
