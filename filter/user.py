from database import find_books
from buttons import get_pagination_button
PEG_NEXT = 10

def full_text_button(data, page):
    """
    Har bir sahifada 10 tadan kitob nomini chiqaradi (matn ko‘rinishida)
    """
    start_index = (page - 1) * PEG_NEXT
    end_index = start_index + PEG_NEXT
    books = data[start_index:end_index]

    text = f"📖 Natijalar — {page}/{(len(data)-1)//PEG_NEXT + 1}\n\n"
    for idx, book in enumerate(books, start=start_index + 1):
        text += f"{idx}. {book[1]}\n"
    return text

def get_all_books(text, search_name, page=1):  
    data = find_books(search_name, text)
    if not data:
        return "😔 Hech narsa topilmadi.", None

    full_text = full_text_button(data, page)
    pagination_buttons = get_pagination_button(data=data, search_name=search_name, text=text, page=page)

    return full_text, pagination_buttons


