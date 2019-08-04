#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from models import db
from datetime import datetime


class BlogCategory(db.Model):
    __tablename__ = 'blog_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    cat_rank = db.Column(db.Integer, nullable=False, default=1)
    cat_level = db.Column(db.Integer, nullable=False, default=1)


class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(300), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    url_id = db.Column(db.String(12), nullable=False)
    content_path = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('blogs', order_by='Blog.create_time'))
    cat_id = db.Column(db.Integer, db.ForeignKey('blog_category.id'))
    category = db.relationship('BlogCategory', backref=db.backref('blogs', order_by='Blog.create_time'))
