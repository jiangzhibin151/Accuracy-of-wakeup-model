# -*- coding: utf-8 -*-
# wakeup.py

import json
import simplejson
import subprocess
from run import csrf
from lib.files import *
from lib.config import *
from flask import request
from flask import redirect, url_for
from lib.upload_file import uploadfile
from views.login import login_required
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template


wakeup = Blueprint('wakeup', __name__,
                url_prefix = '/wakeup',
                template_folder='templates',
                static_folder='static')


@csrf.exempt
@wakeup.route('/wakeup', methods=["GET", "POST"])
@login_required
# wakeup test
def wakeup_index():
    if request.method == 'POST':
        threshold = request.form['threshold']
        radio_wakeup = request.form['radio_value']

        if threshold and radio_wakeup:
            info_list = []
            file_name = DATA_AREA + g.name + 'wakeup'
            result_path = DATA_AREA + g.name + RESULT_PATH
            os.system("rm -rf {}".format(result_path))
            shell_script = "{0} {1} {2}".format(file_name, threshold, radio_wakeup)
            shell_info = subprocess.Popen(['./wakeup_test/wakeup_test_check1.sh ' + shell_script], stdout = subprocess.PIPE, shell = True).stdout.read()
            shell_info = str(shell_info).split(r"\n")
            for i in shell_info:
                if i == "":
                    continue
                info_list.resultend(i.replace(r"\t", " "))
            return render_template('wakeup/wakeup_test.html', info = info_list)

        return render_template('wakeup/wakeup_test.html', info = ["Hi, 缺少参数!"])
    return render_template('wakeup/wakeup_test.html')

@csrf.exempt
@wakeup.route("/wakeup_upload", methods=['GET', 'POST'])
# wakeup file upload
def WakeupUpload():
    if request.method == 'POST':
        files = request.files['file']
        if files:
            filename = secure_filename(files.filename) #check file name
            filename = SetupFileName(filename)
            file_type = files.content_type

            if not CheckFileType(files.filename):
                result = uploadfile(name=filename, type=file_type, size=0, not_allowed_msg="文件类型不允许")
            else:
                if filename.endswith(".pcm"):
                    dir_name = g.name + PCM_SRC
                    dir_name = os.path.join(DATA_AREA, dir_name)
                else:
                    dir_name = g.name + CONFIG_SRC
                    dir_name = os.path.join(DATA_AREA, dir_name)

                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                uploaded_file_path = os.path.join(dir_name, filename)
                files.save(uploaded_file_path)
                size = os.path.getsize(uploaded_file_path)
                result = uploadfile(name=filename, type=file_type, size=size)
            return simplejson.dumps({"files": [result.get_file()]})

    if request.method == 'GET':
        files = ''
        if not os.path.exists(WAKEUP_FOLDER):
            return redirect(url_for('index'))
        for f in os.listdir(WAKEUP_FOLDER):
            if os.path.isfile(os.path.join(WAKEUP_FOLDER, f)):
                files = f
    return  redirect(url_for("wakeupindex"))




# del wakeup file
@csrf.exempt
@wakeup.route("/DelFile/<data>", methods=['GET', 'POST'])
def DelFile(data):
    dir_head = DATA_AREA + request.cookies.get("remember_token").split("|")[0] + "_wakeup/"
    pcm_head = DATA_AREA + g.name + PCM_SRC
    result_head = DATA_AREA + g.name + RESULT_PATH
    data1 = json.loads(data)
    key, = data1

    if key == "del":
        if len(data1[key]) == 0:
            return "亲，没有文件可以删除！"

        for name in data1[key]:
            file_name = name.split("*")
            abs_file = os.path.join((dir_head + file_name[0]), file_name[-1])
            if os.path.exists(abs_file):
                os.remove(abs_file)
        return "删除成功!!!"

    if key == "pcm":
        file_set = set(data1[key])
        pcm_list = []
        if os.path.exists(pcm_head):
            pcm_list = os.listdir(pcm_head)

        for name in file_set:
            file_name = name.split("*")

            if file_name[-1] in pcm_list:
                pcm_list.remove(file_name[-1])

        for i in pcm_list:
            pcm_file = os.path.join(pcm_head, i.strip())
            if os.path.exists(pcm_file):
                os.remove(pcm_file)
        return "删除成功!!!"

    if key == "result":
        file_set = set(data1[key])
        result_list = []
        if os.path.exists(result_head):
            result_list = os.listdir(result_head)

        for name in file_set:
            file_name = name.split("*")

            if file_name[-1] in result_list:
                result_list.remove(file_name[-1])

        for i in result_list:
            result_file = os.path.join(result_head, i.strip())
            if os.path.exists(result_file):
                os.remove(result_file)
        return "删除成功!!!"

    return "删除失败,请重试！"

# clear wakeup file
@csrf.exempt
@wakeup.route("/clear_wakeup", methods=['GET'])
def clear_wakeup():
    dir_head = DATA_AREA + g.name + WAKEUP_SRC
    os.system("rm -rf {}/*".format(dir_head)) #unix
    return render_template('result/wakeup_file_upload.html')