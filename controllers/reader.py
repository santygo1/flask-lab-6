from flask import render_template, redirect, url_for, request

from app import app
from utils import get_db_connection
from models import reader_model


@app.get('/readers/create-form')
def create_reader_form():
    return render_template('new_reader.html')


@app.post('/readers')
def create_reader():
    conn = get_db_connection()
    reader_name = request.values.get("reader_name")

    created_reader_id = reader_model.create_reader(conn, reader_name)

    conn.close()
    return redirect(url_for('index', reader=created_reader_id))


@app.post('/readers/<reader_id>/books/borrow')
def reader_borrow_book(reader_id):
    con = get_db_connection()
    book_id = request.values.get('book_id')

    reader_model.borrow_book(con, reader_id, book_id)

    con.close()
    return redirect(url_for('index', reader=reader_id))


@app.post('/readers/<reader_id>/books/return')
def reader_return_book(reader_id):
    con = get_db_connection()

    book_reader_id = int(request.values.get('return'))
    reader_model.return_book(con, book_reader_id)

    con.close()
    return redirect(url_for('index', reader=reader_id))
