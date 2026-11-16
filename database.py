import sqlite3



def init_db():
    connection = sqlite3.connect('books_db.db')
    cursor = connection.cursor()

    cursor.execute('PRAGMA foreign_keys = ON;')

    cursor.execute('''CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    name TEXT,
    writer TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS books_details(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    genre TEXT,
    FOREIGN KEY (book_id) REFERENCES books (book_id)
    )''')

def add_book(book_id, name, writer, genre):
    connection = sqlite3.connect('books_db.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO books (book_id, name, writer) VALUES (?, ?, ?)',
    (book_id, name, writer))
    cursor.execute('INSERT INTO books_details (book_id, genre) VALUES (?, ?)',
    (book_id, genre))

    connection.commit()
    connection.close()

def get_all_books():
    connection = sqlite3.connect('books_db.db')
    cursor = connection.cursor()
    
    cursor.execute('''
    SELECT books.book_id, books.name, books.writer, books_details.genre
    FROM books
    INNER JOIN books_details ON books.book_id = books_details.book_id
    ''')
    books = cursor.fetchall()
    
    connection.close()
    return books