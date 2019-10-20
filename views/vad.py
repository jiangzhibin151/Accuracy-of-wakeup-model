# -*- coding: utf-8 -*-
# vad.py

import json
import simplejson
import subprocess
from run import csrf
from lib.files import *
from lib.config import *
from views.login import login_required
from lib.upload_file import uploadfile
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, request

vad = Blueprint('vad', __name__,
                url_prefix = '/vad',
                template_folder='templates',
                static_folder='static')

@vad.route('/vad_index/<info>', methods=["get", "post"])
@csrf.exempt
@login_required
def vad_index(info):
    session = request.remote_addr.replace(".", '')
    vad_dir = DATA_AREA + session + "_" + VAD_PATH
    pcm_list = []
    if os.path.exists(vad_dir):
        file_list = os.listdir(vad_dir)
        for i in file_list:
            if i.endswith(".pcm"):
                pcm_list.append(i)
    if info == '#':
        return render_template('vad/vad_test.html', pcm_list = pcm_list)
    return render_template('vad/vad_test.html', pcm_list = pcm_list, info = [info])

@vad.route("vad_clear", methods=['GET'])
@csrf.exempt
@login_required
def vad_clear():
    session = request.remote_addr.replace(".", '')
    dir_head = DATA_AREA + session + "_" + VAD_PATH
    os.system("rm -rf {}/*".format(dir_head)) #unix
    return render_template('vad/vad_file_upload.html')

@vad.route("DelVADFile/<data>", methods=['GET', 'POST'])
@csrf.exempt
@login_required
def DelVADFile(data):
    data1 = json.loads(data)
    if len(data1) == 0:
        return "亲，请选择文件!!!"

    session = request.remote_addr.replace(".", '')
    dir_head = DATA_AREA + session + "_"
    for name in data1:
        abs_dir_path = os.path.join((dir_head + VAD_PATH), name)
        if os.path.exists(abs_dir_path):
            os.remove(abs_dir_path)

    return "文件删除成功!!!"

@vad.route('vad_file_upload/', methods=["GET", "POST"])
@csrf.exempt
@login_required
def vad_file_upload():
    return render_template('vad/vad_file_upload.html')

@vad.route("vadFile", methods=['GET', 'POST'])
def vadFile():
    session = request.remote_addr.replace(".", '')
    if request.method == 'POST':
        files = request.files['file']
        if files:
            filename = secure_filename(files.filename) #check file name
            filename = SetupFileName1(filename)
            file_type = files.content_type

            if not CheckFileType(files.filename):
                vad = uploadfile(name=filename, type=file_type, size=0, not_allowed_msg="文件类型不允许")
            else:
                dir_name = session + "_" + VAD_PATH
                dir_name = os.path.join(DATA_AREA, dir_name)
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)

                uploaded_file_path = os.path.join(dir_name, filename)
                files.save(uploaded_file_path)
                size = os.path.getsize(uploaded_file_path)
                vad = uploadfile(name=filename, type=file_type, size=size)
            return simplejson.dumps({"files": [vad.get_file()]})

    if request.method == 'GET':
        files = ''
        if not os.path.exists(VAD_PATH):
            return redirect(url_for('index'))
        for f in os.listdir(VAD_PATH):
            if os.path.isfile(os.path.join(VAD_PATH, f)):
                files = f
    return redirect(url_for("/vad/file_upload"))


@vad.route('vad_test', methods=["get", "post"])
@csrf.exempt
@login_required
def vad_test():
    session = request.remote_addr.replace(".", '')
    if request.method == 'POST':
        file_list = []
        pcm_name = request.form.get('comp_select')
        start_time = request.form.get('start')
        end_time = request.form.get('end')
        threshold = request.form.get('th')
        if not pcm_name:
            return render_template("vad/vad_test.html", info = ["Hi! 缺少文件!"])

        vad_dir = DATA_AREA + session + "_" + VAD_PATH
        if os.path.exists(vad_dir):
            file_list = os.listdir(vad_dir)

        model_name = ''
        for i in file_list:
            name = i.strip()
            if name.endswith(".q"):
                model_name = name

        shell_script = ""
        if start_time and end_time:
            shell_script = "LD_LIBRARY_PATH=. ./vad_test ../{0} ../{1} {2} {3} {4}"\
                .format(pcm_name, model_name, start_time, end_time, threshold)
        else:
            shell_script = "LD_LIBRARY_PATH=. ./vad_test ../{0} ../{1} 4000 400 {2}"\
                .format(pcm_name, model_name, threshold)

        if model_name:
            info_list = []
            png_path1 = session + "_" + VAD_PATH
            png_path = os.path.join(vad.root_path, os.path.join('static/png/', png_path1))
            os.system("mkdir {} -p".format(png_path))
            vad_test_path = os.path.join(vad_dir, ".vad_test")
            if os.path.exists(vad_test_path):
                os.system("rm -rf {}".format(vad_test_path))

            os.system("cp -r ./vad {}".format(vad_test_path))
            os.system("rm -rf {}/*".format(png_path))

            info = subprocess.Popen(shell_script, shell=True, cwd=vad_test_path,
                                    stdout = subprocess.PIPE).stdout.read()
            os.system("touch {0}/{1}.txt".format(png_path, pcm_name))
            vad_pcm_name = pcm_name.split(".pcm")[0] + '#' + '.pcm'
            vad_shell = "python3 vad_plot.py ../{0} {1} {2}"\
                .format(vad_pcm_name, png_path, pcm_name.split(".pcm")[0])
            p = subprocess.Popen(vad_shell, shell=True, cwd=vad_test_path, stdout = subprocess.PIPE)
            if p.wait() == 0:
                for f in os.listdir(vad_dir):
                    if f.endswith('#.pcm'):
                #        vad.logger.info(f)
                        os.system("rm -rf {}".format(os.path.join(vad_dir, f)))
                shell_info = str(info).split(r"\n")
                for i in shell_info:
                    if i == "":
                        continue
                    info_list.append(i.replace(r"\t", ""))

                return redirect(url_for("vad",info = info_list))
        return redirect(url_for("vad",info = ['Hi! 缺少参数或者文件!']))
    return redirect(url_for("vad"))

