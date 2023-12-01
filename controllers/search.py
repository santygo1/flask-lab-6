from flask import render_template, request

from app import app
from models import search_model
from utils import get_db_connection


@app.get('/search')
def search():
    selected_authors = request.values.getlist("author[]", type=int)
    selected_genres = request.values.getlist("genre[]", type=int)
    selected_publishers = request.values.getlist("publisher[]", type=int)

    conn = get_db_connection()
    genres = search_model.findall_genres_with_count(conn)
    authors = search_model.findall_authors_with_count(conn)
    publishers = search_model.findall_publisher_with_count(conn)

    books = search_model.findall_book_with_filter(conn,
                                                  selected_genres,
                                                  selected_authors,
                                                  selected_publishers)

    conn.close()

    return render_template(
        'search.html',
        df_books=books,
        df_genres=genres,
        df_publishers=publishers,
        df_authors=authors,
        selected_genres=selected_genres,
        selected_publishers=selected_publishers,
        selected_authors=selected_authors
    )
