#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from controllers.main import *
from models.blog_model import Blog, BlogCategory
from configs.fileserver_config import *
from utils import *

from werkzeug.utils import secure_filename
from pypinyin import lazy_pinyin
import os


def init_blog_db():
    blog1 = Blog(title="954.二倍数对数组")
    blog1.url_id = gen_blog_url_id()

    cat1 = BlogCategory(name="LeetCode")
    cat2 = BlogCategory(name="Python3")
    cat3 = BlogCategory(name="AI&ML")
    cat4 = BlogCategory(name="C++")

    blog1.category = cat1

    db.session.add_all([blog1])
    db.session.add_all([cat1, cat2, cat3, cat4])
    db.session.commit()


@main.route('/blogs/')
def blogs_record():
    # init_blog_db()

    cat_list = BlogCategory.query.filter().all()
    cat_all = cat_list
    blogs_list = []
    for cat in cat_list:
        blogs = cat.blogs
        blogs_list.append(blogs)

    dicts = {
        'cat_all': cat_all,
        'cat_list': cat_list,
        'blogs_list': blogs_list,
    }
    return render_template('blog/blog.html', **dicts)


@main.route('/blogs/category/<note_catid>/')
def blogs_cat(note_catid):
    cat_all = BlogCategory.query.filter().all()
    cat = BlogCategory.query.filter(BlogCategory.id == int(note_catid)).first()
    cat_list = []
    cat_list.append(cat)

    blogs_list = []
    blogs = cat.blogs
    blogs_list.append(blogs)

    dicts = {
        'cat_all': cat_all,
        'cat_list': cat_list,
        'blogs_list': blogs_list
    }
    return render_template('blog/blog.html', **dicts)


@main.route('/blogs/doc/<url_id>/')
def blog_detail(url_id):
    cat_all = BlogCategory.query.filter().all()
    blog_local = Blog.query.filter(Blog.url_id == url_id).first()
    title = blog_local.title
    if blog_local.content_path:
        path = str(blog_local.content_path)
        md_data = sec_readfile(path)
    else:
        md_data = '## 该文档不存在！'

    dicts = {
        'cat_all': cat_all,
        'note_cat': blog_local.category,
        'title': title,
        'md_data': md_data,
        'is_blog': 1
    }
    return render_template('notes/note_detail.html', **dicts)


@main.route('/blogs/delete/<cat_id>/<url_id>/', methods=['POST'])
def del_blog(cat_id, url_id):
    blog_local = Blog.query.filter(Blog.url_id == url_id).first()
    if os.path.exists(blog_local.content_path):
        try:
            os.remove(blog_local.content_path)
        except OSError:
            pass

    db.session.delete(blog_local)
    db.session.commit()
    if int(cat_id) == -1:
        return redirect(url_for('main.blogs_record'))
    else:
        return redirect(url_for('main.blogs_cat', note_catid=int(cat_id)))


@main.route('/blogs/edit/<cat_id>/<url_id>/', methods=['GET', 'POST'])
def edit_blog(cat_id, url_id):
    cat_all = BlogCategory.query.filter().all()
    blog_local = Blog.query.filter(Blog.url_id == url_id).first()
    modify_flag = False

    if request.method == 'GET':
        note_content = ""
        if blog_local.content_path:
            path = str(blog_local.content_path)
            note_content = sec_readfile(path)

        dicts = {
            'cat_all': cat_all,
            'note_cat': blog_local.category,
            'catid': cat_id,
            'editBlog': blog_local,
            'doccontent': note_content
        }
        return render_template('blog/edit_blog.html', **dicts)
    else:
        if request.form.get("newTitle"):
            new_title = request.form.get("newTitle")
            blog_local.title = new_title
            modify_flag = True

        if request.form.get("updateContent"):
            # 保存编辑内容
            update_content = request.form.get("updateContent")
            note_cat = blog_local.category
            path = FILESERVER + PATHSEP + 'blogs' + PATHSEP
            path = path + str(note_cat.id) + secure_filename(''.join(lazy_pinyin(note_cat.name))) + PATHSEP
            full_filename = path + secure_filename(''.join(lazy_pinyin(blog_local.title))) + '.md'

            if not os.path.exists(full_filename):
                if blog_local.content_path:
                    try:
                        os.remove(blog_local.content_path)
                    except OSError:
                        pass

            dir_path = os.path.dirname(full_filename)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            blog_local.content_path = full_filename
            sec_writefile(full_filename, update_content)
            modify_flag = True

        # 更新数据库表
        if modify_flag:
            db.session.commit()

        if int(cat_id) == -1:
            return redirect(url_for('main.blogs_record'))
        else:
            return redirect(url_for('main.blogs_cat', note_catid=int(cat_id)))


@main.route('/blogs/create/<cat_id>/', methods=['GET', 'POST'])
def create_blog(cat_id):
    if request.method == 'GET':
        cat_all = BlogCategory.query.filter().all()
        blog_cat = BlogCategory.query.filter(BlogCategory.id == int(cat_id)).first()

        dicts = {
            'cat_all': cat_all,
            'note_cat': blog_cat,
            'catid': cat_id
        }
        return render_template('blog/create_blog.html', **dicts)
    else:
        title = request.form.get('docTitle')
        if title:
            new_blog = Blog(title=title)
            new_blog.url_id = gen_blog_url_id()

            username = session.get('username')
            # 指定用户
            if username:
                user = User.query.filter(User.username == username).first()
            else:
                user = User.query.filter().first()
            new_blog.user = user
            # 设定类别
            note_cat = BlogCategory.query.filter(BlogCategory.id == int(cat_id)).first()
            new_blog.category = note_cat

            # 记录内容
            content = request.form.get('docContent')
            path = FILESERVER + PATHSEP + 'blogs' + PATHSEP + cat_id + secure_filename(''.join(lazy_pinyin(note_cat.name))) + PATHSEP
            full_filename = path + secure_filename(''.join(lazy_pinyin(title))) + '.md'
            if not os.path.exists(path):
                os.makedirs(path)
            sec_writefile(full_filename, content)
            new_blog.content_path = full_filename
            # 更新数据库
            db.session.add(new_blog)
            db.session.commit()

        return redirect(url_for('main.blogs_cat', note_catid=int(cat_id)))
