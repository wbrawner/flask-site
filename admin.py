from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Blueprint
from flask.ext.mysqldb import MySQL
import datetime

admin = Blueprint('admin', __name__,
                        template_folder='templates')
import flask_site

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
        g.db.execute('SELECT * FROM blog_posts ORDER BY updated_on DESC')
        entries = [dict(title=row[1],  category=row[3], tags=row[4], created=row[6].strftime("%d-%m-%Y"), updated=row[7].strftime("%d-%m-%Y")) for row in g.db.fetchall()]
        return render_template('admin/posts.html', entries=entries)

@admin.route('/new-post', methods=['GET', 'POST'])
def new_post():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            g.db.execute("insert into blog_posts (title, text, category, tags, url, created_on, updated_on) values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')" .format(request.form['title'], request.form['text'], request.form['category'], request.form['tags'], request.form['title'].lower().replace(' ', '-'), str(datetime.datetime.now()), str(datetime.datetime.now())))
            flask_site.mysql.connection.commit()
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
            flask_site.mysql.connection.commit()
            flash('New post added successfully')
            return redirect(url_for('blog'))
        else:
            return render_template('admin/new-post.html')