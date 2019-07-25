#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from controllers.main import *
from models.book_model import Book, Author, Year
from sqlalchemy import desc


def init_book_db():
    # book1 = Book(title='平凡的世界')
    # book2 = Book(title='人生')
    # book3 = Book(title='活着')
    # book4 = Book(title='大江大河')
    # book5 = Book(title='百年孤独')
    bookReading1 = Book(title='侯卫东官场笔记')
    bookReading2 = Book(title='激荡三十年')

    # author1 = Author(name="路遥", state="中")
    # author2 = Author(name="余华", state="中")
    # author3 = Author(name="宋运辉", state="中")
    # author4 = Author(name="加西亚.马尔克斯", state="哥")
    authorRead1 = Author(name="侯卫东", state="中")
    authorRead2 = Author(name="吴晓波", state="中")

    # year1 = Year(year=2016)
    # year2 = Year(year=2018)
    # year3 = Year()
    yearRead = Year(year=9999)

    # book1.author = author1
    # book1.year = year1
    # book2.author = author1
    # book2.year = year1
    # book3.author = author2
    # book3.year = year1
    # book4.author = author3
    # book4.year = year3
    # book5.author = author4
    # book5.year = year2

    bookReading1.author = authorRead1
    bookReading1.year = yearRead
    bookReading2.author = authorRead2
    bookReading2.year = yearRead

    db.session.add_all([bookReading1, bookReading2])
    db.session.add_all([authorRead1, authorRead2])
    db.session.add_all([yearRead])
    db.session.commit()


@main.route('/reading/')
def reading():
    # init_book_db()
    return redirect(url_for('main.reading_cat', year=9999))


@main.route('/reading/<year>/')
def reading_cat(year):
    year_all = Year.query.filter().order_by(desc(Year.year)).all()
    year = Year.query.filter(Year.year == int(year)).first()

    dicts = {
        'year_all': year_all,
        'activeYear': year
    }

    return render_template('reading.html', **dicts)


@main.route('/book/create/<year_id>', methods=['GET', 'POST'])
def create_book(year_id):
    if request.method == 'GET':
        year_all = Year.query.filter().order_by(desc(Year.year)).all()
        year = Year.query.filter(Year.year == int(year_id)).first()

        dicts = {
            'year_all': year_all,
            'activeYear': year
        }
        return render_template('book/create_book.html', **dicts)
    else:
        pass


@main.route('/edit_book/<year_id>/<book_id>', methods=['GET', 'POST'])
def edit_book(year_id, book_id):
    book_local = Book.query.filter(Book.id == int(book_id)).first()
    if request.method == 'GET':
        year_all = Year.query.filter().order_by(desc(Year.year)).all()
        year = Year.query.filter(Year.year == int(year_id)).first()

        dicts = {
            'year_all': year_all,
            'activeYear': year,
            'book': book_local
        }
        return render_template('book/edit_book.html', **dicts)
    else:
        pass
