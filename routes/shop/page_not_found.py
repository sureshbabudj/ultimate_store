from flask import render_template
from . import shop

@shop.errorhandler(404)
def page_not_found(e=None):
    return render_template('404.html'), 404

@shop.route('/under_construction')
def under_construction():
    return render_template('404.html'), 404