
@result.route('/login', methods=["GET", 'POST'])
def login():
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
    return render_template('login.html', title="Sign In", form=form)

@result.route('/logout')
@login_required
#flask-login源码config.py里面修改提示信息
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))