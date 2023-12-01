from app import app
from flask import render_template, request, session

from utils import get_db_connection
from models import reader_model


@app.get('/')
def index():
    conn = get_db_connection()
    # нажата кнопка Найти
    if request.values.get('reader'):
        reader_id = int(request.values.get('reader'))
        session['reader_id'] = reader_id

    # вошли первый раз
    else:
        session['reader_id'] = 1

    df_reader = reader_model.find_all(conn)
    df_book_reader = reader_model.find_by_id(conn, session['reader_id'])

    conn.close()

    # выводим форму
    return render_template(
        'index.html',
        reader_id=session['reader_id'],
        combo_box=df_reader,
        book_reader=df_book_reader
    )
