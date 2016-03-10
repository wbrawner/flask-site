from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from flask.ext.mysqldb import MySQL
import hashlib
from flask_debugtoolbar import DebugToolbarExtension
from admin import admin
from flask.ext.mail import Mail, Message
from wtforms import Form, TextField, TextAreaField, validators

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = app.config['SECRET_KEY']
mysql = MySQL(app)
toolbar = DebugToolbarExtension(app)
mail = Mail(app)

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

class ContactForm(Form):
    name = TextField('Name', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    message = TextAreaField('Message', [validators.Length(min=6, max=5000)])

@app.route('/')
def home():
    g.db.execute('SELECT * FROM blog_posts ORDER BY updated_on DESC')
    entries = [dict(title=row[1], text=row[2], url=row[5], created=row[6].strftime("%B %d, %Y"), updated=row[7].strftime("%B %d, %Y")) for row in g.db.fetchall()]
    return render_template('home.html', entries=entries)

@app.route('/bio')
def bio():
    return render_template('bio.html')

@app.route('/blog')
def blog():
    g.db.execute('SELECT * FROM blog_posts ORDER BY id DESC')
    entries = [dict(title=row[1], text=row[2], url=row[5], created=row[6].strftime("%B %d, %Y"), updated=row[7].strftime("%B %d, %Y")) for row in g.db.fetchall()]
    return render_template('blog.html', entries=entries)

@app.route('/blog/<url>')
def blog_post(url):
    g.db.execute('SELECT * FROM blog_posts WHERE url="%s"' % url)
    row = g.db.fetchone()
    post = [dict(title=row[1], text=row[2], category=row[3], tags=row[4], created=row[6].strftime("%B %d, %Y"), updated=row[7].strftime("%B %d, %Y"))]
    return render_template('blog-post.html', post=post)

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        msg = Message(subject='New Message From wbrawner.com',
            body="Name: {0}\nEmail: {1}\nMessage: {2}".format(request.form['name'], request.form['email'], request.form['message']),
            recipients=["billybrawner@gmail.com"])
        mail.send(msg)
        flash('Thanks, your message was sent.')
        return redirect(url_for('contact'))
    else:
        return render_template('contact.html', form=form)

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
    app.run(host= '0.0.0.0')
