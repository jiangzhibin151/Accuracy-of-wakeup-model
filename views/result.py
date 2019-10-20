# -*- coding: utf-8 -*-
# result.py

import shutil
import zipfile
import collections
from run import csrf
from run import cache
from lib.files import *
from lib.config import *
from views.login import login_required
from flask import request, Response, send_from_directory, flash
from flask import Blueprint, render_template, redirect, url_for

result = Blueprint('result', __name__,
                url_prefix = '/result',
                template_folder='templates',
                static_folder='static')

@result.route('/check_result/<type>', methods=["get"])
@csrf.exempt
@login_required
def check_result(type):
    if type == "wakeup":
        head = DATA_AREA + g.name
        result_file = DATA_AREA + g.name + result.config["RESULT_SRC"]
        nowakeup_file = DATA_AREA + g.name + NOWAKEUP_SRC
        result_path = DATA_AREA + g.name + RESULT_PATH
        result_file_list, nowakeup_file_list, nowakeup_dic = [], [], {}
        if os.path.exists(result_file):
            with open(result_file, "r") as r1:
                result_file_list = r1.readlines()

        os.system("rm -rf {}*dir".format(head))
        os.system("rm -rf {}*.zip".format(head))

        list1 = []
        if os.path.exists(nowakeup_file):
            with open(nowakeup_file, "r") as r2:
                list1 = r2.readlines()
        if list1:
            for i in list1:
                name = i.split("/")[-1]
                path = i.split(name)[0]
                nowakeup_file_list.resultend([path, name])
            return  render_template("wakeup_test_result.html", result_file_list = result_file_list,
                                    nowakeup_file_list = nowakeup_file_list)
        else:
            if os.path.exists(result_path):
                alist = os.listdir(result_path)
                for i in alist:
                    if i.endswith(".pcm"):
                        nowakeup_file_list.resultend(i)
                return  render_template("unwakeup_test_result.html", result_file_list = result_file_list,
                                        nowakeup_file_list = nowakeup_file_list)

    img_abspath = collections.OrderedDict()
    if type == "plot":
        png_path1 = g.name + PLOT_SRC
        pcm_name = ''
        clear_plotdir(png_path1)
        png_path = os.path.join('static/png/', png_path1)
        if os.path.exists(png_path):
            img_list = os.listdir(png_path)
            for i in img_list:
                if i.endswith(".png"):
                    img_abspath[i] = os.path.join(png_path, i.strip())
                elif i.endswith(".pcm.txt"):
                    pcm_name = i.strip(".txt")
        else:
            img_abspath["没有生成概率图"] = ""
        if "二级模型.png" in img_abspath.keys():
            img_abspath.move_to_end("二级模型.png")
        if "第二级模型[整条].png" in img_abspath.keys():
            img_abspath.move_to_end("第二级模型[整条].png")

        return render_template("result/demo_test_result.html", img_abspath = img_abspath,
                               pcm_name = pcm_name)

    if type == "vad":
        session = request.remote_addr.replace(".", '')
        png_path1 = session + "_" + VAD_PATH
        pcm_name = ''
        clear_plotdir(png_path1)
        png_path = os.path.join('static/png/', png_path1)
        if os.path.exists(png_path):
            img_list = os.listdir(png_path)
            for i in img_list:
                if i.endswith(".png"):
                    img_abspath[i] = os.path.join(png_path, i.strip())
                elif i.endswith(".pcm.txt"):
                    pcm_name = i.strip(".txt")

        return render_template("result/vad_test_result.html", img_abspath = img_abspath,
                               pcm_name = pcm_name)

    return render_template("result/wakeup_test_result.html")

# download no wakeup file
@cache.memoize(timeout=1)
@csrf.exempt
@result.route('/download/<path:filename>', methods = ["GET", "POST"])
@login_required
def download(filename):
    Response.Buffer = True
    # Response.ExpiresAbsolute = Now() - 1
    Response.Expires = 0
    Response.CacheControl ="no-cache"
    result_path = DATA_AREA + g.name + RESULT_PATH
    head = DATA_AREA + g.name
    dirpath = os.path.join(result.root_path, (head + PCM_SRC))
    nowakeup_file = head + NOWAKEUP_SRC
    pcm_file = head + PCM_SRC
    pcm_list = []
    nowakeup_dir = ''
    nowakeup_zip = ''
    target_path = ''

    if filename == "nowakeup_all":
        nowakeup_list = []
        if os.path.exists(nowakeup_file):
            with open(nowakeup_file, "r") as r1:
                nowakeup_list = r1.readlines()

        target_path = head + "nowakeup_dir"
        nowakeup_zip = head + "nowakeup.zip"
        os.system("mkdir -p {}".format(target_path))
        if nowakeup_list:
            for i in nowakeup_list:
                shutil.copy(i.strip(), target_path)

        zipf = zipfile.ZipFile(nowakeup_zip, 'w')
        pre_len = len(os.path.dirname(target_path))
        for parent, dirnames, filenames in os.walk(target_path):
            for filename in filenames:
                pathfile = os.path.join(parent, filename)
                arcname = pathfile[pre_len:].strip(os.path.sep)
                zipf.write(pathfile, arcname)
        zipf.close()
        return send_from_directory(result.root_path, filename = nowakeup_zip, as_attachment=True)

    if filename == "wakeup_all":
        target_path = head + "wakeup_dir"
        nowakeup_zip = head + "wakeup.zip"
        os.system("mkdir -p {}".format(target_path))
        pcm_list = os.listdir(result_path)
        for i in pcm_list:
            i = i.strip()
            if i.endswith(".pcm"):
                source_path = os.path.join(result_path, i)
                shutil.copy(source_path, target_path)

        zipf = zipfile.ZipFile(nowakeup_zip, 'w')
        pre_len = len(os.path.dirname(target_path))
        for parent, dirnames, filenames in os.walk(target_path):
            for filename in filenames:
                pathfile = os.path.join(parent, filename)
                arcname = pathfile[pre_len:].strip(os.path.sep)
                zipf.write(pathfile, arcname)
        zipf.close()
        return send_from_directory(result.root_path, filename=nowakeup_zip, as_attachment=True)

    if os.path.getsize(nowakeup_file):
        file_dir = filename.split("**")
        if os.path.exists(os.path.join(file_dir[1], file_dir[2])):
            return send_from_directory(file_dir[1], filename = file_dir[2], as_attachment=True)
        flash('文件已经被移除!')
        return render_template("wakeup_test_result.html")
    else:
        dir_name = os.path.join(os.getcwd(), (head + RESULT_PATH))
        if os.path.exists(os.path.join(dir_name, filename)):
            return send_from_directory(dir_name, filename = filename.strip(), as_attachment=True)
        flash('文件已经被移除!')
        return render_template("wakeup_test_result.html")
    return redirect(url_for("check_result"))

def clear_plotdir(png_path1):
    png_path = os.path.join('static/png/', png_path1)
    source_png_path = os.path.join((DATA_AREA + png_path1), ".plot_test/png_result/")
    if not os.path.exists(png_path):
        os.mkdir(png_path)
    file_list = []
    if os.path.exists(source_png_path):
        file_list = os.listdir(source_png_path)
    for i in file_list:
        if i.endswith(".png") or i.endswith(".pcm.txt"):
            img_path = os.path.join(source_png_path, i.strip())
            if os.path.exists(img_path):
                shutil.copy(img_path, png_path)

def delete_cache():
    cache.clear()