#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from controllers.main import *
from models.notes_model import Note, NoteCategory
from configs.fileserver_config import *
from utils import *

from werkzeug.utils import secure_filename
from pypinyin import lazy_pinyin
import datetime
import os


def init_note_db():
    note1 = Note(title="test-刘慈欣访谈")

    cat1 = NoteCategory(name="人物访谈类")
    cat2 = NoteCategory(name="心得体会类")
    cat3 = NoteCategory(name="生活类")

    note1.category = cat1

    db.session.add_all([note1])
    db.session.add_all([cat1, cat2, cat3])
    db.session.commit()


@main.route('/notes/')
def notes_record():
    # init_note_db()

    cat_list = NoteCategory.query.filter().order_by(NoteCategory.cat_rank).all()
    # cat_all = cat_list
    cat_all = classify_by_rank(cat_list)
    # print("After, len = %s" % len(cat_all))

    notes_list = []
    for cat in cat_list:
        notes = cat.notes
        notes_list.append(notes)

    dicts = {
        'cat_all': cat_all,
        'cat_list': cat_list,
        'notes_list': notes_list,
    }
    return render_template('notes/notes.html', **dicts)


@main.route('/notes/category/<note_catid>/')
def notes_cat(note_catid):
    cat_all = classify_by_rank(NoteCategory.query.filter().order_by(NoteCategory.cat_rank).all())
    cat = NoteCategory.query.filter(NoteCategory.id == int(note_catid)).first()
    cat_list = []
    cat_list.append(cat)

    notes_list = []
    notes = cat.notes
    notes_list.append(notes)

    dicts = {
        'cat_all': cat_all,
        'cat_list': cat_list,
        'notes_list': notes_list
    }
    return render_template('notes/notes.html', **dicts)


@main.route('/notes/detail/<note_id>/')
def note_detail(note_id):
    cat_all = classify_by_rank(NoteCategory.query.filter().order_by(NoteCategory.cat_rank).all())
    note_local = Note.query.filter(Note.id == int(note_id)).first()
    title = note_local.title
    if note_local.content_path:
        path = str(note_local.content_path)
        md_data = sec_readfile(path)
    else:
        md_data = '## 该文档不存在！'

    dicts = {
        'cat_all': cat_all,
        'note_cat': note_local.category,
        'title': title,
        'md_data': md_data
    }
    return render_template('notes/note_detail.html', **dicts)


@main.route('/notes/delete/<cat_id>/<note_id>/', methods=['POST'])
def del_note(cat_id, note_id):
    note_local = Note.query.filter(Note.id == int(note_id)).first()
    if os.path.exists(note_local.content_path):
        try:
            os.remove(note_local.content_path)
        except OSError:
            pass

    db.session.delete(note_local)
    db.session.commit()
    if int(cat_id) == -1:
        return redirect(url_for('main.notes_record'))
    else:
        return redirect(url_for('main.notes_cat', note_catid=int(cat_id)))


@main.route('/notes/edit/<cat_id>/<note_id>/', methods=['GET', 'POST'])
def edit_note(cat_id, note_id):
    cat_all = classify_by_rank(NoteCategory.query.filter().order_by(NoteCategory.cat_rank).all())
    note_local = Note.query.filter(Note.id == int(note_id)).first()
    modify_flag = False

    if request.method == 'GET':
        note_content = ""
        if note_local.content_path:
            path = str(note_local.content_path)
            note_content = sec_readfile(path)

        dicts = {
            'cat_all': cat_all,
            'note_cat': note_local.category,
            'catid': cat_id,
            'editNote': note_local,
            'doccontent': note_content
        }
        return render_template('notes/edit_note.html', **dicts)
    else:
        if request.form.get("newTitle"):
            new_title = request.form.get("newTitle")
            note_local.title = new_title
            modify_flag = True

        if request.form.get("updateContent"):
            # 保存编辑内容
            update_content = request.form.get("updateContent")
            note_cat = note_local.category
            path = FILESERVER + PATHSEP + 'notes' + PATHSEP
            path = path + str(note_cat.id) + secure_filename(''.join(lazy_pinyin(note_cat.name))) + PATHSEP
            full_filename = path + secure_filename(''.join(lazy_pinyin(note_local.title))) + '.md'

            if not os.path.exists(full_filename):
                if note_local.content_path:
                    try:
                        os.remove(note_local.content_path)
                    except OSError:
                        pass

            dir_path = os.path.dirname(full_filename)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            note_local.content_path = full_filename
            sec_writefile(full_filename, update_content)
            modify_flag = True

        # 更新数据库表
        if modify_flag:
            db.session.commit()

        if int(cat_id) == -1:
            return redirect(url_for('main.notes_record'))
        else:
            return redirect(url_for('main.notes_cat', note_catid=int(cat_id)))


@main.route('/notes/create/<cat_id>/', methods=['GET', 'POST'])
def create_note(cat_id):
    if request.method == 'GET':
        cat_all = classify_by_rank(NoteCategory.query.filter().order_by(NoteCategory.cat_rank).all())
        note_cat = NoteCategory.query.filter(NoteCategory.id == int(cat_id)).first()

        dicts = {
            'cat_all': cat_all,
            'note_cat': note_cat,
            'catid': cat_id
        }
        return render_template('notes/create_note.html', **dicts)
    else:
        title = request.form.get('docTitle')
        if title:
            new_note = Note(title=title)
            username = session.get('username')
            # 指定用户
            if username:
                user = User.query.filter(User.username == username).first()
            else:
                user = User.query.filter().first()
            new_note.user = user
            # 设定类别
            note_cat = NoteCategory.query.filter(NoteCategory.id == int(cat_id)).first()
            new_note.category = note_cat

            # 记录内容
            content = request.form.get('docContent')
            path = FILESERVER + PATHSEP + 'notes' + PATHSEP + cat_id + secure_filename(''.join(lazy_pinyin(note_cat.name))) + PATHSEP
            full_filename = path + secure_filename(''.join(lazy_pinyin(title))) + '.md'
            if not os.path.exists(path):
                os.makedirs(path)
            sec_writefile(full_filename, content)
            new_note.content_path = full_filename
            # 更新数据库
            db.session.add(new_note)
            db.session.commit()

        return redirect(url_for('main.notes_cat', note_catid=int(cat_id)))


@main.route('/upload/', methods=['POST'])
def upload():
    file = request.files.get('editormd-file')
    if not file:
        result = {
            'success': 0,
            'message': '上传失败'
        }
    else:
        filename, upload_time = request.form.get('filename'), request.form.get('upload-time')
        filedir = os.path.join(FILESERVER, "md_files")
        if file.mimetype.find('image') >= 0:
            file_type = "image"
            fn_2 = upload_time + '-' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + os.path.splitext(filename)[1]
            filename = fn_2
        else:
            file_type = "files"
        # print(filename)
        filedir = os.path.join(filedir, file_type)
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        file.save(os.path.join(filedir, filename))
        result = {
            'success': 1,
            'message': '上传成功!',
            'filename': filename,
            'filetype': file_type,
            'url': url_for('main.image', type=file_type, name=filename)
        }
    return jsonify(result)


@main.route('/md/<type>/<name>', methods=['GET'])
def image(type, name):
    filedir = os.path.join(FILESERVER, "md_files", type)
    # with open(os.path.join(filedir, name), 'rb') as f:
    #     resp = Response(f.read(), mimetype="image/jpeg")
    # return resp
    return send_from_directory(filedir, filename=name)
