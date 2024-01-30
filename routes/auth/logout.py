from flask import redirect, url_for, flash
from flask_login import login_required, logout_user
from . import auth

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('shop.home'))