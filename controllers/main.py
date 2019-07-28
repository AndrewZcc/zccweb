#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from flask import Blueprint, render_template, request, session, redirect, url_for
from models.user_model import db, User
from sqlalchemy import and_

main = Blueprint('main', __name__)


@main.route('/')
def index():
    # return redirect(url_for('main.reading'))
    # return redirect(url_for('main.poetry'))
    return redirect(url_for('main.notes_record'))


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

