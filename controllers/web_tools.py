#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from controllers.main import main
from flask import render_template, redirect, url_for, request, flash
from configs.fileserver_config import *
import os, xmltodict, re


@main.route('/product/infos/')
def product_infos():
    rpm_list = dict()
    rpm_list["a.rpm"] = {"name": "a.rpm", "md5sum": "21aef2", "size": "100K"}
    rpm_list["b.rpm"] = {"name": "b.rpm", "md5sum": "43aef4", "size": "123K"}
    return render_template('webtools/product_info.html', rpm_list=rpm_list)


@main.route('/product/test/')
def temp_test():
    return render_template('webtools/js_adjust_pageContent.html')


@main.route('/search/rpm', methods=['GET', 'POST'])
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
        search_restype = {}
        search_resowner = {}
        for version in search_version:
            xml_root = root_dir + os.sep + version
            res_rpm = []
            res_rpmtype = []
            res_rpmowner = []
            for main_dir, subdir, rpm_file_list in os.walk(xml_root):
                for rpm_file in rpm_file_list:
                    if rpm_file.startswith("rpm"):
                        xml_path = xml_root + os.sep + rpm_file
                        with open(xml_path) as fd:
                            xml = xmltodict.parse(fd.read())
                            packages = xml["filelists"]["package"]
                            for pack in packages:
                                pack.setdefault("file", [])
                                files = pack["file"]
                                for file in files:
                                    # Regular Expression Match
                                    reg = so_file_name.replace(".", "\\.")
                                    try:
                                        regular = re.search(reg, str(file))
                                    except Exception:
                                        regular = None
                                    # print("match-reg: %s" % reg)
                                    if regular:
                                        # print(">>> %s" % regular)
                                        rpm_file_name = pack["@name"]
                                        res_rpm.append(rpm_file_name + ".rpm")
                                        res_rpmtype.append(rpm_file.split('.')[0][14:])
                                        res_rpmowner.append("owner-zcc.")
                                        break

            if len(res_rpm) != 0:
                search_res[version] = res_rpm
                search_restype[version] = res_rpmtype
                search_resowner[version] = res_rpmowner

        dicts = {
            'dirs': dirs,
            'active_v': b_version,
            'so_file': so_file_name,
            'search_res': search_res,
            'search_restype': search_restype,
            'search_resowner': search_resowner
        }

        if not len(search_res):
            flash("error")
        else:
            flash("ok")
        return render_template('webtools/rpmsearch.html', **dicts)
