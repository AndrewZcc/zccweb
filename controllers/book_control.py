#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from controllers.main import *
from models.book_model import Book, Author, Year
from sqlalchemy import desc
from configs.fileserver_config import *
from werkzeug.utils import secure_filename
from pypinyin import lazy_pinyin
from utils import *
import os


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


@main.route('/book/<year_id>/<book_id>')
def book_detail(year_id, book_id):
    year_all = Year.query.filter().order_by(desc(Year.year)).all()
    year = Year.query.filter(Year.year == int(year_id)).first()
    book = Book.query.filter(Book.id == int(book_id)).first()

    if book.mdNotePath:
        path = str(book.mdNotePath)
        md_data = sec_readfile(path)
    else:
        md_data = '## 该文档不存在！'

    dicts = {
        'year_all': year_all,
        'activeYear': year,
        'title': book.title,
        'md_data': md_data
    }
    return render_template('book/book_detail.html', **dicts)


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
        book_title = request.form.get('bookTitle')
        if book_title:
            new_book = Book(title=book_title)

            book_desc = request.form.get('bookTitleDesc')
            if book_desc:
                new_book.title_desc = book_desc

            author = request.form.get('bookAuthor')
            author_state = request.form.get('bookAuthorState')
            book_author = Author(name=author, state=author_state)
            new_book.author = book_author

            book_year = Year.query.filter(Year.year == int(year_id)).first()
            if not book_year:
                book_year = Year(year=int(year_id))
                db.session.add(book_year)
            new_book.year = book_year

            book_image = request.form.get('bookImgLink')
            if book_image:
                new_book.imagePath = book_image

            oneSentence = request.form.get('bookOneSentence')
            if oneSentence:
                new_book.one_sentence = oneSentence

            eBookPath = request.form.get('eBookPath')
            if eBookPath:
                new_book.eBookPath = eBookPath

            # 记录读后感
            content = request.form.get('docContent')
            if content:
                path = FILESERVER + '/reading/' + year_id + "/"
                full_filename = path + secure_filename(''.join(lazy_pinyin(book_title))) + '.md'
                if not os.path.exists(path):
                    os.makedirs(path)
                sec_writefile(full_filename, content)
                new_book.mdNotePath = full_filename

            # 更新数据库
            db.session.add(book_author)
            db.session.add(new_book)
            db.session.commit()

        return redirect(url_for('main.reading_cat', year=year_id))


@main.route('/edit_book/<year_id>/<book_id>', methods=['GET', 'POST'])
def edit_book(year_id, book_id):
    book_local = Book.query.filter(Book.id == int(book_id)).first()
    modify_flag = False

    if request.method == 'GET':
        year_all = Year.query.filter().order_by(desc(Year.year)).all()
        year = Year.query.filter(Year.year == int(year_id)).first()

        note_content = ""
        if book_local.mdNotePath:
            path = str(book_local.mdNotePath)
            note_content = sec_readfile(path)

        dicts = {
            'year_all': year_all,
            'activeYear': year,
            'book': book_local,
            'noteContent': note_content
        }
        return render_template('book/edit_book.html', **dicts)
    else:
        if request.form.get("newTitle"):
            new_title = request.form.get("newTitle")
            book_local.title = new_title
            modify_flag = True

        if request.form.get('updateContent'):
            updateContent = request.form.get('updateContent')
            path = FILESERVER + '/reading/' + year_id + "/"
            full_filename = path + secure_filename(''.join(lazy_pinyin(book_local.title))) + '.md'

            if not os.path.exists(full_filename):
                if book_local.mdNotePath:
                    try:
                        os.remove(book_local.mdNotePath)
                    except OSError:
                        pass

            dir_path = os.path.dirname(full_filename)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            book_local.mdNotePath = full_filename
            sec_writefile(full_filename, updateContent)
            modify_flag = True

        # 更新数据库表
        if modify_flag:
            db.session.commit()

        return redirect(url_for('main.reading_cat', year=year_id))
