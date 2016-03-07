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

@admin.route('/posts')
def posts():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('admin/posts.html')

@admin.route('/new-post', methods=['GET', 'POST'])
def new_post():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            g.db.execute('insert into blog_posts (title, text, category, tags, created_on, updated_on) values (?, ?, ?, ?, str(datetime.datetime.now()), str(datetime.datetime.now()))',
            [request.form['title'], request.form['text'], request.form['category'], request.form['tags']])
            g.db.commit()
            flash('New post added successfully')
            return redirect(url_for('blog'))
        else:
            return render_template('admin/new-post.html')

@admin.route('/edit-post', methods=['GET', 'POST'])
def edit_post():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            g.db.execute('UPDATE blog_posts SET (title, text, category, tags, updated_on) values (?, ?, ?, ?,  str(datetime.datetime.now()))',
            [request.form['title'], request.form['text'], request.form['category'], request.form['tags']])
            g.db.commit()
            flash('New post added successfully')
            return redirect(url_for('blog'))
        else:
            return render_template('admin/new-post.html')