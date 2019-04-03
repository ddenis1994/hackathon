from flask import Flask, template_rendered, flash, request, render_template
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore,login_user,current_user
from flask_mail import Mail
from DBLocal.database import db_session, init_db, Session
from DBLocal.models import User, Role
import numpy as np
import sounddevice as sd
from flask_sqlalchemy import SQLAlchemy

# Create app
app = Flask(__name__)
mail = Mail(app)
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
    user_datastore.create_user(email='matt@nobien.net', password='password')
    db_session.commit()




@app.route('/register')
def register_page():
    return render_template('security/register_user.html')


@app.route('/login')
def login_page():
    return render_template('security/login_user.html')


@app.route('/')
@login_required
def index():
    if current_user.is_authenticated:
        if 'ADMIN' in current_user.roles:
            return render_template('status/admin_login.html')
        if 'MANAGER' in current_user.roles:
            return render_template('status/parent_login.html')
        return render_template('status/normal_login.html')
    return index()


def login(user_name, password):
    result = User.query.filter_by(username=user_name).first()
    if result == "None":
        flash("wrong user name", category="login")
        return index()
    if result.password == password:
        return index()


def register(user, password, permissions, Email):
    user_datastore.create_user(username=user, password=password, email=Email)
    user_datastore.add_role_to_user(user=user, role=permissions)
    db_session.commit()
    login_user(User.query.filter_by(username=user).first())
    return index()


@app.route('/handle_data', methods=['POST'])
def handle_data():
    # redirect the date for the correct func
    if request.form['type_form'] == 'login':
        return login(request.form['inputIdMain'], request.form['inputPasswordMain'])
    elif request.form['type_form'] == 'register':
        return register(request.form['Register_New_User'], request.form['Register_New_Password'],request.form['permissions'],request.form['Email'])
    return index()



duration = 3  # in seconds
volume_list = []


def audio_callback(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    volume_list.append(int(volume_norm))
    # print(int(volume_norm))


stream = sd.InputStream(callback=audio_callback)
with stream:
    sd.sleep(duration * 1000)
    # print(sum(volume_list)/len(volume_list))
    print(max(volume_list))



if __name__ == '__main__':
    app.config.from_object('config.Production.ProductionConfig')
    app.run()
