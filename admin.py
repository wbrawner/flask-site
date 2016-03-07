from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Blueprint
from flask.ext.mysqldb import MySQL

admin = Blueprint('admin', __name__,
                        template_folder='templates')

@admin.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('admin/home.html')