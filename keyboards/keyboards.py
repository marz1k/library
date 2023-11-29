from aiogram import types


def menu():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton(text='Посмотреть все книги', callback_data='get_books'),
        types.InlineKeyboardButton(text='Найти книгу', callback_data='find_book'),
    )
    keyboard.add(
        types.InlineKeyboardButton(text='Добавить кингу', callback_data='add_book')
    )
    return keyboard


def books_kb(books, page, search=False):
    keyboard = types.InlineKeyboardMarkup()
    print(books[page*10:page*10+10])
    for book in books[page*10:page*10+10]:
        print(book)
        keyboard.add(
            types.InlineKeyboardButton(text=f'{book["name"]} | {book["author"]}', callback_data=f"book_{str(book['book_id'])}")
        )
    if search is False:
        keyboard.row(
            types.InlineKeyboardButton(text='<<<', callback_data='page_back'),
            types.InlineKeyboardButton(text=page, callback_data='page_num'),
            types.InlineKeyboardButton(text='>>>', callback_data='page_next'),
        )
        keyboard.row(
            types.InlineKeyboardButton(text='В меню', callback_data='to_menu'),
            types.InlineKeyboardButton(text='Поиск по жанру', callback_data='genre_search')
        )
    else:
        keyboard.add(
            types.InlineKeyboardButton(text='В меню', callback_data='to_menu'),
        )
    return keyboard


def book_options(book_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text='Удалить книгу', callback_data=f"delete_{book_id}")
    )
    keyboard.add(
        types.InlineKeyboardButton(text='Назад к списку', callback_data=f"back_to_list")
    )
    return keyboard


def genres_kb(genres):
    print(genres)
    keyboard = types.InlineKeyboardMarkup()
    if len(genres) > 0:
        for genre in genres:
            keyboard.add(
                types.InlineKeyboardButton(text=f'{genre["genre"]}',
                                           callback_data=f"gnr_{genre['genre']}")
            )
        return keyboard

    else:
        keyboard.add(
            types.InlineKeyboardButton(text=f'Готовых жанров нету',
                                       callback_data=f"no")
        )


def confirm():
    keyboards = types.InlineKeyboardMarkup()
    keyboards.row(
        types.InlineKeyboardButton(text='Добавить✅', callback_data='add_confirm'),
        types.InlineKeyboardButton(text='Отмена❌', callback_data="add_cancel")
    )
    return keyboards

