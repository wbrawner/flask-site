from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from flask.ext.mysqldb import MySQL
import hashlib
from admin import admin

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = app.config['SECRET_KEY']
mysql = MySQL(app)

app.register_blueprint(admin, url_prefix='/admin')

def connect_db():
    return  mysql.connection.cursor()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    g.db.execute('SELECT * FROM blog_posts ORDER BY updated_on DESC')
    entries = [dict(title=row[1], text=row[2], created=row[5].strftime("%B %d, %Y"), updated=row[6].strftime("%B %d, %Y")) for row in g.db.fetchall()]
    return render_template('home.html', entries=entries)

@app.route('/bio')
def bio():
    return render_template('bio.html')

@app.route('/blog')
def blog():
    g.db.execute('SELECT * FROM blog_posts ORDER BY id DESC')
    entries = [dict(title=row[1], text=row[2], created=row[5].strftime("%B %d, %Y"), updated=row[6].strftime("%B %d, %Y")) for row in g.db.fetchall()]
    return render_template('blog.html', entries=entries)

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif hashlib.sha512(request.form['password'].encode('utf-8')).hexdigest() != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('admin.home'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('blog'))

if __name__ == '__main__':
    app.run()
