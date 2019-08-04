#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from models.blog_model import *
import random, string


def generate_random_str(randomlength=16):
    """
    string.digits=0123456789
    string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    """
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str


def gen_blog_url_id(length=12):
    url_id = generate_random_str(length)
    while 1:
        blog = Blog.query.filter(Blog.url_id == url_id).first()
        if not blog:
            break
        url_id = generate_random_str(length)

    return url_id


def classify_by_rank(cat_list):
    record = 0
    cat_all = []
    cats = []

    for c in cat_list:
        if int(c.cat_rank) // 100 == record:
            # print("Record[%s]: name: %s, cat_rank: %s" % (record, c.name, c.cat_rank))
            cats.append(c)
        else:
            cat_all.append(cats)
            record += 1
            # cats.clear()
            cats = []
            cats.append(c)

    if len(cats) != 0:
        cat_all.append(cats)

    return cat_all
