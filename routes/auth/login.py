from flask import render_template, redirect, url_for, flash
from flask_login import login_user
from forms import LoginForm
from models import User
from . import auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Check credentials and login user
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('shop.home'))

        flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)

