#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from controllers.main import main
from flask import render_template, redirect, url_for, request, flash
from configs.fileserver_config import *
import os, xmltodict


@main.route('/search/rpm2so/', methods=['GET', 'POST'])
def search_rpm():
    root_dir = FILESERVER + os.sep + "webtools"
    dirs = ""
    for res in os.walk(root_dir):
        dirs = sorted(res[1], reverse=True)
        break

    if request.method == "GET":
        return render_template('webtools/rpmsearch.html', dirs=dirs)
    else:
        so_file_name = request.form.get("soFileName")
        b_version = request.values.get("bVersion")
        # print("so: %s, bv: %s" % (so_file_name, b_version))
        if (not so_file_name) or (not b_version):
            flash("error_input")
            return render_template('webtools/rpmsearch.html', dirs=dirs)

        search_version = []
        if b_version == "All":
            search_version = dirs
        else:
            search_version.append(b_version)

        search_res = {}
        for version in search_version:
            xml_path = root_dir + os.sep + version + os.sep + "rpm-file-list.xml"
            res_rpm = []
            with open(xml_path) as fd:
                xml = xmltodict.parse(fd.read())
                packages = xml["filelists"]["package"]
                for pack in packages:
                    files = pack["file"]
                    for file in files:
                        if str(file).find(so_file_name) >= 0:
                            rpm_file_name = pack["@name"]
                            # print("so: %s, rpm: %s" % (so_file_name, rpm_file_name))
                            res_rpm.append(rpm_file_name + ".rpm")
                            break
            if len(res_rpm) != 0:
                search_res[version] = res_rpm

        dicts = {
            'dirs': dirs,
            'active_v': b_version,
            'so_file': so_file_name,
            'search_res': search_res
        }

        if not len(search_res):
            flash("error")
        else:
            flash("ok")
        return render_template('webtools/rpmsearch.html', **dicts)
