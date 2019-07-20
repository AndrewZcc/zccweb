#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from flask import Blueprint, render_template, request, session, redirect, url_for
from models.user_model import db, User
from models.book_model import Book, Author, Year
from sqlalchemy import and_

main = Blueprint('main', __name__)


def init_db():
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
    #init_db()

    years = Year.query.filter().all()
    books = Book.query.filter().all()

    dicts = {
        'years': years,
        'books': books
    }

    return render_template('reading.html', **dicts)


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


@main.route('/poetry/')
def poetry():
    return render_template('poetry.html')
