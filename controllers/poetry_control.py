#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from controllers.main import *
from models.poetry_model import Poetry, Poeter, PoetryCategory
from utils.file_operation import *
from configs.fileserver_config import *
from werkzeug.utils import secure_filename
from pypinyin import lazy_pinyin
import os


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
    cat_all = cat_list
    poetries_list = []
    for cat in cat_list:
        poetries = cat.poetries
        poetries_list.append(poetries)

    dicts = {
        'cat_all': cat_all,
        'cat_list': cat_list,
        'poetries_list': poetries_list
    }
    return render_template('poetry.html', **dicts)


@main.route('/poetry/category/<poet_catid>/')
def poetry_cat(poet_catid):
    cat_all = PoetryCategory.query.filter().all()
    cat = PoetryCategory.query.filter(PoetryCategory.id == int(poet_catid)).first()
    poetries = cat.poetries

    cat_list = []
    cat_list.append(cat)
    poetries_list = []
    poetries_list.append(poetries)

    dicts = {
        'cat_all': cat_all,
        'cat_list': cat_list,
        'poetries_list': poetries_list
    }
    return render_template('poetry.html', **dicts)


@main.route('/poetry/<poetry_id>/')
def poetry_detail(poetry_id):
    cat_all = PoetryCategory.query.filter().all()
    poetry_local = Poetry.query.filter(Poetry.id == int(poetry_id)).first()
    title = poetry_local.title
    if poetry_local.content_path:
        path = str(poetry_local.content_path)
        md_data = sec_readfile(path)
    else:
        md_data = '## 该文档不存在！'

    poet_cat = poetry_local.categories[0]

    dicts = {
        'cat_all': cat_all,
        'poet_cat': poet_cat,
        'title': title,
        'md_data': md_data
    }
    return render_template('poetry/detail.html', **dicts)


@main.route('/del_poetry/<cat_id>/<poetry_id>/', methods=['POST'])
def del_poetry(cat_id, poetry_id):
    poetry_local = Poetry.query.filter(Poetry.id == int(poetry_id)).first()
    db.session.delete(poetry_local)
    db.session.commit()
    if int(cat_id) == -1:
        return redirect(url_for('main.poetry'))
    else:
        return redirect(url_for('main.poetry_cat', poet_catid=int(cat_id)))


@main.route('/edit_poetry/<cat_id>/<poetry_id>/', methods=['GET', 'POST'])
def edit_doc(cat_id, poetry_id):
    poetry_local = Poetry.query.filter(Poetry.id == int(poetry_id)).first()
    doc_title = poetry_local.title
    doc_id = poetry_local.id
    modify_flag = False

    if request.method == 'GET':
        doc_content = ""
        if poetry_local.content_path:
            path = str(poetry_local.content_path)
            doc_content = sec_readfile(path)

        dicts = {
            'catid': cat_id,
            'docid': doc_id,
            'doctitle': doc_title,
            'doccontent': doc_content
        }
        return render_template('poetry/edit_poetry.html', **dicts)
    else:
        if request.form.get("newTitle"):
            new_title = request.form.get("newTitle")
            poetry_local.title = new_title
            modify_flag = True

        if request.form.get("updateContent"):
            # 保存编辑内容
            update_content = request.form.get("updateContent")
            poet_cat = poetry_local.categories[0]
            path = FILESERVER + '/poetry/' + str(poet_cat.id) + secure_filename(
                ''.join(lazy_pinyin(poet_cat.name))) + "/"
            full_filename = path + secure_filename(''.join(lazy_pinyin(doc_title))) + '.md'

            if not os.path.exists(full_filename):
                if poetry_local.content_path:
                    try:
                        os.remove(poetry_local.content_path)
                    except OSError:
                        pass

            dir_path = os.path.dirname(full_filename)
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)

            poetry_local.content_path = full_filename
            sec_writefile(full_filename, update_content)
            modify_flag = True

        # 更新数据库表
        if modify_flag:
            db.session.commit()

        if int(cat_id) == -1:
            return redirect(url_for('main.poetry'))
        else:
            return redirect(url_for('main.poetry_cat', poet_catid=int(cat_id)))


@main.route('/poetry/create/<cat_id>/', methods=['GET', 'POST'])
def create_poetry(cat_id):
    if request.method == 'GET':
        return render_template('poetry/create_poetry.html', catid=cat_id)
    else:
        title = request.form.get('docTitle')
        if title:
            content = request.form.get('docContent')
            poet_name = request.form.get('docAuthor')
            poet_state = request.form.get('docAuthorState')

            new_poetry = Poetry(title=title)
            # 指定诗人
            poet = Poeter.query.filter(and_(Poeter.name == poet_name, Poeter.state == poet_state)).first()
            if not poet:
                poet = Poeter(name=poet_name, state=poet_state)
            new_poetry.poet = poet
            # 设定类别
            poet_cat = PoetryCategory.query.filter(PoetryCategory.id == int(cat_id)).first()
            new_poetry.categories.append(poet_cat)
            # 记录内容
            path = FILESERVER + '/poetry/' + cat_id + secure_filename(''.join(lazy_pinyin(poet_cat.name))) + "/"
            full_filename = path + secure_filename(''.join(lazy_pinyin(title))) + '.md'
            if not os.path.exists(path):
                os.mkdir(path)
            sec_writefile(full_filename, content)
            new_poetry.content_path = full_filename
            # 更新数据库
            db.session.add(new_poetry)
            db.session.commit()

        return redirect(url_for('main.poetry_cat', poet_catid=int(cat_id)))
