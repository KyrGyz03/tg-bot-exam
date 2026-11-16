from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from database import add_book, get_all_books

router = Router()

class AddBook(StatesGroup):
    waiting_num = State()
    waiting_name = State()
    waiting_writer = State()
    waiting_genre = State()


@router.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}")


@router.message(Command('add_book'))
async def start_add_book(message: Message, state: FSMContext):
    await message.answer('Номер книги (Цифрами): ')
    await state.set_state(AddBook.waiting_num)


@router.message(AddBook.waiting_num)
async def process_book_num(message: Message, state: FSMContext):
    if message.text and message.text.isdigit():
        await message.answer('Теперь название книги: ')
        await state.update_data(book_id=int(message.text))
        await state.set_state(AddBook.waiting_name)
    else:
        await message.answer('Ошибка, нужно вводить только числа')
        return


@router.message(AddBook.waiting_name)
async def process_book_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Теперь, кто автор этой книги? ')
    await state.set_state(AddBook.waiting_writer)


@router.message(AddBook.waiting_writer)
async def process_book_writer(message: Message, state: FSMContext):
    await state.update_data(writer=message.text)
    await message.answer('Какой жанр этой книги? ')
    await state.set_state(AddBook.waiting_genre)


@router.message(AddBook.waiting_genre)
async def process_book_genre(message: Message, state: FSMContext):
    await state.update_data(genre=message.text)
    data = await state.get_data()

    add_book(
        book_id=data['book_id'],
        name=data['name'],
        writer=data['writer'],
        genre=data['genre'],
    )

    await message.answer(
        f"--Книга добавлена--\n"
        f"Номер: {data['book_id']}\n"
        f"Название: {data['name']}\n"
        f"Автор: {data['writer']}\n"
        f"Жанр: {data['genre']}"
    )
    await state.clear()

@router.message(Command('books'))
async def show_books(message: Message):
    await message.answer('Список книг: ')
    books = get_all_books()
    if not books:
        await message.answer('Список пуст')
        return

    text = '--Список книг--'
    for book in books:
        book_id, name, writer, genre = book

        await message.answer(
            f'Номер книги: {book_id}\n'
            f'Название: {name}\n'
            f'Автор: {writer}\n'
            f'Жарн: {genre}'
        )
