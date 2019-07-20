#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from flask import Blueprint, render_template, request, session, redirect, url_for
from models.user_model import db, User
from models.book_model import Book, Author, Year
from models.poetry_model import Poetry, Poeter, PoetryCategory
from sqlalchemy import and_

main = Blueprint('main', __name__)


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


@main.route('/')
def index():
    #init_book_db()

    #return redirect(url_for('main.reading'))
    return redirect(url_for('main.poetry'))


@main.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        checkbox = request.form.get('checkbox')

        user = User.query.filter(and_(User.username == username,
                                      User.password == password)).first()
        if user:
            session['username'] = username
            if checkbox:
                session.permanent = True
                print('[Info] set session permanent = true!')
            return redirect(url_for('main.index'))
        else:
            print('[Info] 用户名或密码错误！')
            return redirect(url_for('main.login'))


@main.route('/logout/')
def logout():
    if session['username']:
        session.pop('username')
    return redirect(url_for('main.index'))


@main.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter(User.username == username).first()

        if user:
            return '用户已存在！请重新注册！'
        else:
            if password1 != password2:
                return '两次密码输入不一致，请确认后再重新注册！'
            else:
                session['username'] = username
                user = User(username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('main.index'))


# TODO: 使用 全局 g 对象
# TODO: 向全局传递 selected_navbar, years, poetry_categories 信息
# TODO: base.html 可通过访问 g对象 动态生成 侧边栏！
# TODO: 替代方案：使用 session (不推荐)！


@main.route('/reading/')
def reading():
    years = Year.query.filter().all()
    books = Book.query.filter().all()

    dicts = {
        'years': years,
        'books': books
    }

    return render_template('reading.html', **dicts)


def init_poetry_db():
    poetry1 = Poetry(title='忠诚')
    poetry2 = Poetry(title='致橡树')
    poetry3 = Poetry(title='雨巷')
    poetry4 = Poetry(title='念奴娇·赤壁怀古')

    poet1 = Poeter(name='何达', state='香港')
    poet2 = Poeter(name='舒婷')
    poet3 = Poeter(name='戴望舒')
    poet4 = Poeter(name='苏轼', state='北宋')

    cat1 = PoetryCategory(name='现代诗')
    cat2 = PoetryCategory(name='宋词')
    cat3 = PoetryCategory(name='唐诗')
    cat4 = PoetryCategory(name='古诗')

    poetry1.poet = poet1
    poetry2.poet = poet2
    poetry3.poet = poet3
    poetry4.poet = poet4

    poetry1.categories.append(cat1)
    poetry2.categories.append(cat1)
    poetry3.categories.append(cat1)
    poetry4.categories.append(cat2)

    db.session.add_all([poetry1, poetry2, poetry3, poetry4])
    db.session.add_all([poet1, poet2, poet3, poet4])
    db.session.add_all([cat1, cat2, cat3, cat4])
    db.session.commit()


@main.route('/poetry/')
def poetry():
    # init_poetry_db()

    cat_list = PoetryCategory.query.filter().all()
    poetries_list = []
    for cat in cat_list:
        poetries = cat.poetries
        poetries_list.append(poetries)

    dicts = {
        'cat_list': cat_list,
        'poetries_list': poetries_list
    }
    return render_template('poetry.html', **dicts)


@main.route('/poetry/category/<poet_catid>/')
def poetry_cat(poet_catid):
    cat = PoetryCategory.query.filter(PoetryCategory.id == int(poet_catid)).first()
    poetries = cat.poetries

    cat_list = []
    cat_list.append(cat)
    poetries_list = []
    poetries_list.append(poetries)

    dicts = {
        'cat_list': cat_list,
        'poetries_list': poetries_list
    }
    return render_template('poetry.html', **dicts)


@main.route('/poetry/<poetry_id>/')
def poetry_detail(poetry_id):
    poetry_local = Poetry.query.filter(Poetry.id == int(poetry_id)).first()
    title = poetry_local.title
    if poetry_local.content_path:
        md_data = '## 有内容 path = %s' % poetry_local.content_path
    else:
        md_data = '## 该文档不存在！'

    dicts = {
        'title': title,
        'md_data': md_data
    }
    return render_template('poetry/detail.html', **dicts)
