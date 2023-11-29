from aiogram.dispatcher import FSMContext
from states.states import *
from keyboards.keyboards import *
from aiogram import types
from loader import dp, bot, db

pages = {}  # user_id:page


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Добро пожаловать в библиотеку📚!', reply_markup=menu())


@dp.callback_query_handler(text='to_menu')
async def to_menu(call: types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.send_message(call.message.chat.id, 'Меню', reply_markup=menu())


@dp.callback_query_handler(text=['get_books', 'back_to_list'])
async def get_books(call: types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    books = await db.select_all_books()
    pages[call.message.chat.id] = 0
    page = pages[call.message.chat.id]
    await bot.send_message(call.message.chat.id, "Книги: ", reply_markup=books_kb(books, page))


@dp.callback_query_handler(text='genre_search')
async def get_books(call: types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    genres = await db.select_all_genres()
    await bot.send_message(call.message.chat.id, 'Жанры', reply_markup=genres_kb(genres))


@dp.callback_query_handler(lambda text: text.data.startswith('gnr'))
async def get_book(call: types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    genre = call.data.split("_")[-1]
    books = await db.select_book_by_genre(genre)
    pages[call.message.chat.id] = 0
    page = pages[call.message.chat.id]
    await bot.send_message(call.message.chat.id, f"{genre}: ", reply_markup=books_kb(books, page, True))



@dp.callback_query_handler(text='page_next')
async def get_books(call: types.CallbackQuery):
    books = await db.select_all_books()
    page = pages[call.message.chat.id]
    if len(books[page*10:page*10+10]) < page*10:
        await call.answer('Последняя страница')
    else:
        pages[call.message.chat.id] += 1
        page = pages[call.message.chat.id]
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=books_kb(books, page))


@dp.callback_query_handler(text='page_back')
async def get_books(call: types.CallbackQuery):
    books = await db.select_all_books()
    page = pages[call.message.chat.id]
    if page == 0:
        await call.answer('Последняя страница')
    else:
        pages[call.message.chat.id] -= 1
        page = pages[call.message.chat.id]
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=books_kb(books, page))


@dp.callback_query_handler(lambda text: text.data.startswith('book'))
async def get_book(call: types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    book_id = int(call.data.split('_')[-1])
    book = await db.select_book_by_id(book_id)
    await bot.send_message(call.message.chat.id, f'Книга:\n\n'
                           f'Название: <b>{book["name"]}</b>'
                           f'\nАвтор: <b>{book["author"]}</b>'
                           f'\nЖанр: <b>{book["genre"]}</b>'
                           f'\nОписание: <b>{book["description"]}</b>',
                           parse_mode='HTML', reply_markup=book_options(book_id))


@dp.callback_query_handler(lambda text: text.data.startswith('delete'))
async def delete_book(call: types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    book_id = int(call.data.split('_')[-1])
    await db.delete_book(book_id)
    await bot.send_message(call.message.chat.id, f'Книга удалена.', parse_mode='HTML', reply_markup=menu())


@dp.callback_query_handler(text='find_book')
async def find_book(call: types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.send_message(call.message.chat.id, 'Введите ключевые слова для поиска книги:')
    await FindBook.phrase.set()


@dp.message_handler(state=FindBook.phrase)
async def find_book(message: types.Message, state: FSMContext):
    await state.finish()
    key = message.text
    books = await db.find_book(key)
    if len(books) != 0:
        page = pages[message.chat.id] = 0
        await message.answer("Книги по ключевым словам: ", reply_markup=books_kb(books, page))
    else:
        await message.answer('Книг не найдено', reply_markup=menu())


@dp.callback_query_handler(text='add_book')
async def add_book(call: types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.send_message(call.message.chat.id, 'Введите название книги: ')
    await AddBook.name.set()


@dp.message_handler(state=AddBook.name)
async def add_book(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer('Введите автора книги: ')
    await AddBook.author.set()


@dp.message_handler(state=AddBook.author)
async def add_book(message: types.Message, state: FSMContext):
    author = message.text
    genres = await db.select_all_genres()
    await state.update_data(author=author)
    await message.answer('Введите жанр книги или выберите из готовых: ', reply_markup=genres_kb(genres))
    await AddBook.genre.set()


@dp.callback_query_handler(state=AddBook.genre)
async def add_book(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(genre=call.data.split("_")[-1])
    await bot.send_message(call.message.chat.id, 'Введите описание книги: ')
    await AddBook.description.set()


@dp.message_handler(state=AddBook.genre)
async def add_book(message: types.Message, state: FSMContext):
    await state.update_data(genre=message.text)
    await message.answer('Введите описание книги')
    await AddBook.description.set()


@dp.message_handler(state=AddBook.description)
async def add_book(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await message.answer(f'Книга: {data["name"]}\n'
                         f'Автор: {data["author"]}\n'
                         f'Жанр: {data["genre"]}\n'
                         f'Описание: {data["description"]}', reply_markup=confirm())
    await AddBook.confirm.set()


@dp.callback_query_handler(state=AddBook.confirm)
async def add_book(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == 'add_confirm':
        data = await state.get_data()
        await db.add_book(name=data['name'],
                          author=data['author'],
                          genre=data['genre'],
                          description=data['description'])
        await bot.send_message(call.message.chat.id, "Книга добавлена", reply_markup=menu())
    else:
        await bot.send_message(call.message.chat.id, "Книга не добавлена", reply_markup=menu())
    await state.finish()
    # print(call.data)


