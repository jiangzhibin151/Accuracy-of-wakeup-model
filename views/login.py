# -*- coding: utf-8 -*-
# login.py

from lib.models import User
from lib.forms import LoginForm
from lib.models import query_user
from flask_login import login_required, login_user, logout_user
from flask import Blueprint, request, flash, render_template, redirect, url_for

login = Blueprint('login', __name__,
                url_prefix = '/login',
                template_folder='templates',
                static_folder='static')

@login.route('/login', methods=["GET", 'POST'])
def login_index():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        user = query_user(user_name)

        if user is not None and password == user['password']:
            curr_user = User()
            curr_user.id = user_name
            login_user(curr_user, remember=True)
            return redirect(request.args.get('next') or url_for('index'))

        flash('用户名或密码错误！')
    return render_template('login/login.html', title="Sign In", form=form)

@login.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))
