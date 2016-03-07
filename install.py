from flask_site import *

def init_db():
    with app.app_context():
        with open('/home/billy/flask-site/schema.sql', 'r') as f:
            g.db = connect_db()
            g.db.execute(f.read())

if __name__ == "__main__":
    init_db()
