# -*- coding: utf-8 -*-
# plot.py

import json
import simplejson
import subprocess
from run import csrf
from lib.files import *
from lib.config import *
from lib.upload_file import uploadfile
from flask_login import login_required
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, request, g

plot = Blueprint('plot', __name__,
                url_prefix = '/plot',
                template_folder='templates',
                static_folder='static')

@plot.route('/plot/<info>', methods=["get", "post"])
@csrf.exempt
@login_required
def plot_index(info):
    pcm_list = []
    plot_dir = DATA_AREA + g.name + PLOT_SRC

    if os.path.exists(plot_dir):
        file_list = os.listdir(plot_dir)
        for i in file_list:
            if i.endswith(".pcm"):
                pcm_list.append(i)
    if info == '$':
        return render_template('plot/plot_test.html', pcm_list = pcm_list)
    return render_template('plot/plot_test.html', pcm_list = pcm_list, info = [info])

@plot.route('/plot_check', methods=["GET", "POST"])
@csrf.exempt
@login_required
def plot_check():
    if request.method == 'POST':
        file_list = []
        pcm_name = request.form.get('comp_select')
        start_time = request.form.get('start')
        end_time = request.form.get('end')
        if not pcm_name:
            return render_template("plot/plot_test.html", info = ["Hi! 缺少文件!"])

        plot_dir = DATA_AREA + g.name + PLOT_SRC
        if os.path.exists(plot_dir):
            file_list = os.listdir(plot_dir)
        plot_name = ''
        for i in file_list:
            name = i.strip()
            if name.endswith(".q") and not name.endswith("2.q"):
                plot_name = name

        shell_script = ""
        if start_time and end_time:
            shell_script = "python3 ./plot_yinsu.py ../{0} ../{1} png_plot/ {2} {3}"\
                .format(pcm_name, plot_name, start_time, end_time)
        else:
            shell_script = "python3 ./plot_yinsu.py ../{0} ../{1} png_plot/ 0 9999999".format(pcm_name, plot_name)

        if plot_name:
            info_list = []
            png_path1 = g.name + PLOT_SRC
            png_path = os.path.join('static/png/', png_path1)
            plot_test_path = os.path.join(plot_dir, ".plot_test")
            if os.path.exists(plot_test_path):
                # Clean up before executing the script plot_test
                os.system("rm -rf {}".format(plot_test_path))

            os.system("cp -r ./wakeup_test/plot_wakeup_ph {}".format(plot_test_path))
            os.system("rm -rf {}/*".format(png_path))

            info = subprocess.Popen(shell_script, shell=True, cwd=plot_test_path,
                                    stdout = subprocess.PIPE).stdout.read()
            # Shows which data is being tested
            os.system("touch {0}/png_plot/{1}.txt".format(plot_test_path, pcm_name))
            shell_info = str(info).split(r"\n")

            for i in shell_info:
                if i == "":
                    continue
                info_list.append(i.replace(r"\t", ""))

            return redirect(url_for("plot", info = info_list))
        return redirect(url_for("plot", info = ["Hi! 缺少文件!"]))
    return redirect(url_for("plot"))

# clear plot file
@plot.route("/clear", methods=['GET'])
@csrf.exempt
@login_required
def clear():
    dir_head = DATA_AREA + g.name + PLOT_SRC
    os.system("rm -rf {}/*".format(dir_head)) #unix
    return render_template('plot/plot_file_upload.html')

# Select del plot check file
@plot.route("/DelAllFile/<data>", methods=['GET', 'POST'])
@csrf.exempt
@login_required
def DelAllFile(data):
    data1 = json.loads(data)
    if len(data1) == 0:
        return "亲，请选择文件!!!"

    dir_head = DATA_AREA + g.name
    for name in data1:
        abs_dir_path = os.path.join((dir_head + PLOT_SRC), name)
        if os.path.exists(abs_dir_path):
            os.remove(abs_dir_path)

    return "文件删除成功!!!"

@plot.route('/plotIndex', methods=["GET", "POST"])
@csrf.exempt
@login_required
def plotIndex():
    return render_template('plot/plot_file_upload.html')

# plot check file upload
@plot.route("/plotFile", methods=['GET', 'POST'])
@csrf.exempt
@login_required
def plotFile():
    if request.method == 'POST':
        files = request.files['file']
        if files:
            filename = secure_filename(files.filename) #check file name
            filename = SetupFileName1(filename)
            file_type = files.content_type

            if not CheckFileType(files.filename):
                plot = uploadfile(name=filename, type=file_type, size=0, not_allowed_msg="文件类型不允许")
            else:
                dir_name = g.name + PLOT_SRC
                dir_name = os.path.join(DATA_AREA, dir_name)
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)

                uploaded_file_path = os.path.join(dir_name, filename)
                files.save(uploaded_file_path)
                size = os.path.getsize(uploaded_file_path)
                plot = uploadfile(name=filename, type=file_type, size=size)
            return simplejson.dumps({"files": [plot.get_file()]})

    if request.method == 'GET':
        files = ''
        if not os.path.exists(PLOT_SRC):
            return redirect(url_for('index'))
        for f in os.listdir(PLOT_SRC):
            if os.path.isfile(os.path.join(PLOT_SRC, f)):
                files = f
    return redirect(url_for("plotIndex"))