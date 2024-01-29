from flask import render_template, redirect, url_for, flash
from flask_login import login_user
from forms import SignUpForm
from models import User, db
from . import auth

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        # Check if the email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email is already in use. Please choose a different one.', 'danger')
            return render_template('signup.html', title='Sign Up', form=form)

        # Process the form data (create a new user and store in the database)
        new_user = User(email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html', title='Sign Up', form=form)