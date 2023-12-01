import pandas, sqlite3


def find_all(conn):
    return pandas.read_sql('''SELECT * FROM reader''', conn)


def find_by_id(conn, reader_id):
    # выбираем и выводим записи о том, какие книги брал читатель
    return pandas.read_sql(
        '''
        WITH get_authors( book_id, authors_name) AS ( 
            SELECT book_id, GROUP_CONCAT(author_name) FROM author 
            JOIN book_author USING(author_id) 
        GROUP BY book_id
        )

        SELECT
            title AS Название,
            authors_name AS Авторы,
            borrow_date AS 'Дата выдачи',
            return_date AS 'Дата возврата',
            book_reader_id
        FROM reader
        JOIN book_reader USING(reader_id)
        JOIN book USING(book_id)
        JOIN get_authors USING(book_id)
        WHERE reader.reader_id = :id
        ORDER BY 3
        ''', conn, params={"id": reader_id})


def create_reader(con, reader_name: str):
    cur = con.cursor()

    cur.execute(f"""
    INSERT INTO reader(reader_name) VALUES 
    ('{reader_name}')
    """)

    created_reader_id = cur.lastrowid
    con.commit()

    return created_reader_id


def borrow_book(conn, reader_id, book_id):
    try:
        cur = conn.cursor()
        cur.executescript(
            f"""
                UPDATE book
                SET available_numbers = available_numbers - 1
                WHERE book_id = {book_id}
            """
        )
        cur.executescript(
            f"""
                INSERT INTO book_reader(book_id, reader_id, borrow_date)  VALUES
                ({book_id}, {reader_id}, DATE('now')) 
            """
        )

        conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        print("Ошибка транзакции")
    pass


def return_book(conn, book_reader_id):
    try:
        cur = conn.cursor()

        book_id = cur.execute(
            f"""
            SELECT book_id FROM book_reader
            WHERE book_reader_id={book_reader_id}
            """
        ).fetchone()

        if book_id is None:
            print("Книга не найдена")
            return

        book_id = book_id[0]

        cur.executescript(
            f"""
                UPDATE book_reader
                SET return_date = DATE('now')
                WHERE book_reader_id = {book_reader_id}
            """
        )
        cur.executescript(
            f"""
                UPDATE book
                SET available_numbers = available_numbers + 1
                WHERE book_id = {book_id}
            """
        )

        conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        print("Ошибка транзакции")
    pass
