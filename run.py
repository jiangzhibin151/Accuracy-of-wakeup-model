#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# run.py

import os
from lib import config
from datetime import timedelta
from flask_caching import Cache
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap
from lib.manager import login_manager
from flask import redirect, url_for, Flask

app = Flask(__name__)
csrf =CSRFProtect()
csrf.init_app(app)
bootstrap = Bootstrap(app)
app.secret_key = os.urandom(24)
app.config.from_object(config)
app.jinja_env.auto_reload = True
login_manager.init_app(app=app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

#一秒刷新一下请求静态文件，防止缓存
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(seconds=1)

# plot check module
from views.plot import plot
app.register_blueprint(plot)

# login module
from views.login import login
app.register_blueprint(login)

# wakeup check module
from views.wakeup import wakeup
app.register_blueprint(wakeup)

# result module
from views.result import result
app.register_blueprint(result)

# vad check module
from views.vad import vad
app.register_blueprint(vad)

# Vad module is login free
@app.route('/', methods=["get", "post"])
def index():
    return redirect(url_for('vad.vad_index', info = '#'))

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port= "6666", debug=True)

