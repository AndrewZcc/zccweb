#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from controllers.main import *
from configs.fileserver_config import *
import os
import time
from flask import make_response, send_from_directory
from xml.dom import minidom

FILE_DIR = os.path.join(FILESERVER, 'guides')


@main.route('/download/<fullname>')
def downloader(fullname):
    filename = fullname.split(os.sep)[-1]
    dirpath = fullname[:-len(filename)]
    print(fullname)
    print(dirpath)
    print(filename)
    return send_from_directory(dirpath, filename, as_attachment=True)


@main.route('/doc/')
@main.route('/doc/<subdir>')
def document(subdir=None):
    if not subdir:
        # 名字为空，切换到根目录
        os.chdir(FILE_DIR)
        subdir = ''
    else:
        # fullname = os.path.join(FILE_DIR, subdir)
        fullname = FILE_DIR + os.sep + subdir
        # if fullname.endswith(os.sep):
        #     fullname = fullname[:-1]

        #  如果是文件，则下载
        if os.path.isfile(fullname):
            return redirect(url_for('main.downloader', fullname=fullname))
        #  如果是目录，切换到该目录下面
        else:
            os.chdir(fullname)

    current_dir = os.getcwd()
    current_list = os.listdir(current_dir)
    contents = []
    for i in sorted(current_list):
        fullpath = current_dir + os.sep + i
        # 如果是目录，在后面添加一个sep
        if os.path.isdir(fullpath):
            extra = os.sep
        else:
            extra = ''
        content = dict()
        content['filename'] = i + extra
        content['mtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(fullpath).st_mtime))
        content['size'] = str(round(os.path.getsize(fullpath) / 1024)) + 'k'
        contents.append(content)
    return render_template('webtools/file_server.html', contents=contents, subdir=subdir, ossep=os.sep)


@main.route('/download/file/')
def file_downloader():
    file_path = FILE_DIR
    filename = "test.xml"

    xml = minidom.Document()
    root = xml.createElement('rpm_delta')

    package_name_delta = xml.createElement('package_name_delta')
    rpm = xml.createElement('rpm')
    rpm.setAttribute('name', 'dophi-ldc-devel')
    package_name_delta.appendChild(rpm)

    package_file_delta = xml.createElement('package_file_delta')
    rpm = xml.createElement('rpm')
    rpm.setAttribute('name', 'c-ares')
    minus_filelist = xml.createElement('minus_filelist')
    file = xml.createElement('file')
    file.setAttribute('name', "usr/bin/adig")
    reason = xml.createElement('reason')
    file.appendChild(reason)
    minus_filelist.appendChild(file)
    rpm.appendChild(minus_filelist)
    package_file_delta.appendChild(rpm)

    root.appendChild(package_name_delta)
    root.appendChild(package_file_delta)

    # print(root.toprettyxml(indent='\t'))

    os.chdir(file_path)
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(root.toprettyxml(indent='\t'))

    response = make_response(
        send_from_directory(file_path, filename.encode('utf-8').decode('utf-8'), as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response


def xml2string(path):
    result = ''
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            result += line
    return result


@main.route('/xml/editor/')
def xml_editor():
    xml_path = os.path.join(FILE_DIR, "delta.xml")
    xml_string = xml2string(xml_path)
    return render_template('webtools/xml_editor.html', xml=xml_string)
