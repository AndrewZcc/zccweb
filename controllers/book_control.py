#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from controllers.main import *
from models.book_model import Book, Author, Year


def init_book_db():
    book1 = Book(title='平凡的世界')
    book2 = Book(title='人生')
    book3 = Book(title='活着')
    book4 = Book(title='大江大河')
    book5 = Book(title='百年孤独')

    author1 = Author(name="路遥", state="中")
    author2 = Author(name="余华", state="中")
    author3 = Author(name="宋运辉", state="中")
    author4 = Author(name="加西亚.马尔克斯", state="哥")

    year1 = Year(year=2016)
    year2 = Year(year=2018)
    year3 = Year()

    book1.author = author1
    book1.year = year1

    book2.author = author1
    book2.year = year1

    book3.author = author2
    book3.year = year1

    book4.author = author3
    book4.year = year3

    book5.author = author4
    book5.year = year2

    db.session.add_all([book1, book2, book3, book4, book5])
    db.session.add_all([author1, author2, author3, author4])
    db.session.add_all([year1, year2, year3])
    db.session.commit()


@main.route('/reading/')
def reading():
    # init_book_db()

    years = Year.query.filter().all()
    books = Book.query.filter().all()

    dicts = {
        'years': years,
        'books': books
    }

    return render_template('reading.html', **dicts)


@main.route('/book/create/<year_id>', methods=['GET', 'POST'])
def create_book(year_id):
    if request.method == 'GET':
        return render_template('book/create_book.html')
    else:
        pass


@main.route('/edit_book/<year_id>/<book_id>', methods=['GET', 'POST'])
def edit_book(year_id, book_id):
    book_local = Book.query.filter(Book.id == int(book_id)).first()
    if request.method == 'GET':
        return render_template('book/edit_book.html', book=book_local)
    else:
        pass
