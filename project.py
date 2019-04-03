from flask import Flask, template_rendered, flash
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore
from DBLocal.database import db_session, init_db, Session
from DBLocal.models import User, Role
from flask_sqlalchemy import SQLAlchemy

# Create app
app = Flask(__name__)
# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session,
                                                User, Role)
security = Security(app, user_datastore)
session = Session()

# Create a user to test with
@app.before_first_request
def create_user():
    init_db()
    #session.add(User(username='admin', email='admin@localhost'))
    #user_datastore.create_user(email='matt@nobien.net', password='password')
    db_session.commit()


# Views
@app.route('/')
@login_required
def home():
    result = User.query.filter_by(username='admin').first()
    return template_rendered('Here you go!')


@app.route('/login_submit')
def login_submit(user_name, password):
    result = User.query.filter_by(username=user_name).first()
    if result == "None":
        flash("wrong user name", category="login")
        return home()
    if result.password == password:
        return index()



if __name__ == '__main__':
    app.config.from_object('config.Production.ProductionConfig')
    app.run()
