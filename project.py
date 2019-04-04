from flask import Flask, flash, request, render_template, Response, stream_with_context
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore, login_user, current_user,logout_user
from flask_mail import Mail
from model.crypto2 import des, des_dicrypte
from DBLocal.database import db_session, init_db, Session
from DBLocal.models import User, Role


# Create app
app = Flask(__name__)
mail = Mail(app)
# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session,
                                                User, Role)
security = Security(app, user_datastore)
session = Session()
key = "NEDDNEDD"

# Create a user to test with
@app.before_first_request
def create_user():
    init_db()
    user_datastore.create_role(name='ADMIN')
    db_session.commit()
    user_datastore.create_user(email='admin', password=des('admin', key), roles=['ADMIN'])
    db_session.commit()



@app.route('/register')
def register_page():
    return render_template('security/register_user.html')


@app.route('/login')
def login_page():
    return render_template('security/login_user.html')

@app.route('/speech')
def speech():
    return render_template('/speech-to-text.html')


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
    result = User.query.filter_by(email=user_name).first()
    if result == None:
        flash("wrong user name", category="login")
        return login_page()
    if des_dicrypte(result.password, key) == password:
        login_user(result)
    return index()


def register(user, password, permissions, Email):
    user_datastore.create_user(username=user, password=des(password, key), email=Email)
    user_datastore.add_role_to_user(user=user, role=permissions)
    db_session.commit()
    login_user(User.query.filter_by(username=user).first())
    return index()


def get_sound():
    return render_template('/')


@app.route('/handle_data', methods=['POST'])
def handle_data():
    # redirect the date for the correct func
    if request.form['type_form'] == 'login':
        return login(request.form['inputIdMain'], request.form['inputPasswordMain'])
    elif request.form['type_form'] == 'register':
        return register(request.form['Register_New_User'], request.form['Register_New_Password'],request.form['permissions'],request.form['Email'])
    elif request.form['type_form'] == 'getSound':
        return getSound()
    return index()


@app.route('/record_page')
def record_page():
    return render_template('/record.html')


@app.route('/logout')
def logout():
    logout_user()
    return index()


if __name__ == '__main__':
    app.config.from_object('config.Production.ProductionConfig')
    app.run()
