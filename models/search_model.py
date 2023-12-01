import pandas


def findall_genres_with_count(conn):
    return pandas.read_sql("""
    SELECT genre.genre_id as id, genre_name as name, count(book_id) as books_count FROM genre
    LEFT OUTER JOIN book b on genre.genre_id = b.genre_id
    GROUP BY b.genre_id
    """, conn)


def findall_authors_with_count(conn):
    return pandas.read_sql("""
    SELECT author.author_id as id, author_name as name, count(book_id) as books_count FROM author
    LEFT OUTER JOIN book_author ba on author.author_id = ba.author_id
    GROUP BY author.author_id
    """, conn)


def findall_publisher_with_count(conn):
    return pandas.read_sql("""
    SELECT publisher.publisher_id as id, publisher_name as name, count(book_id) as books_count FROM publisher
    LEFT OUTER JOIN book b on publisher.publisher_id = b.publisher_id
    GROUP BY b.publisher_id
    """, conn)


def findall_book_with_filter(conn, genre_ids, author_ids, publisher_ids):
    filters = []
    if len(publisher_ids):
        filters.append(f"(publisher_id in({', '.join(map(str, publisher_ids))}))")
    if len(genre_ids):
        filters.append(f"(genre_id in ({', '.join(map(str, genre_ids))}))")
    if len(author_ids):
        filters.append(f"(author_id in ({', '.join(map(str, author_ids))}))")

    filter_expr = " and ".join(filters)

    return pandas.read_sql(
        f'''
        WITH get_books_authors_inline(book_id, authors) AS (
            SELECT book_id, group_concat(author_name, ', ') FROM book_author
            JOIN (SELECT * FROM author ORDER BY author_name) using (author_id)
            GROUP BY book_id
        )
        
        SELECT DISTINCT 
        title as Название,
        genre_name as Жанр,
        authors as Авторы, 
        publisher_name as Издательство,
        year_publication as 'Год издания', 
        available_numbers as Количество,
        book.book_id 
        FROM book
        JOIN publisher using (publisher_id)
        JOIN book_author using (book_id)
        JOIN author using (author_id)
        JOIN genre using (genre_id)
        JOIN get_books_authors_inline using(book_id)
        
        {"WHERE " + filter_expr if len(filter_expr) else ""}
        GROUP BY book_author_id
        ''',
        conn)
