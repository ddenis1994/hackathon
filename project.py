import base64

from flask import Flask, flash, request, render_template, Response, stream_with_context
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore, login_user, current_user
from flask_mail import Mail
from speech_recognition import Microphone
from DBLocal.database import db_session, init_db, Session
from DBLocal.models import User, Role
import speech_recognition as sr


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
    #user_datastore.create_user(email='matt@nobien.net', password='password')
    #db_session.commit()



@app.route('/register')
def register_page():
    return render_template('security/register_user.html')


@app.route('/login')
def login_page():
    return render_template('security/login_user.html')

@app.route('/speech')
def speech():
    return render_template('/speech-to-text.html')



@app.route('/audio', methods=['POST','GET'] )
def audio():
    r = sr.Recognizer()
    data = request.data
    return str(type(data))
    try:
        date=sr.AudioData(data,1,1)
        massge=r.recognize_google(date,None,"he-IL")
    except:
        date=AudioSegment.from_mono_audiosegments(data)
        date=sr.AudioData(date,1,2)
        massge=r.recognize_google(date,None,"he-IL")
    return str(massge)

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
    elif request.form['type_form'] == 'getSound':
        return use_date()
    return index()


@app.route('/record_page')
def record_page():
    return render_template('/record.html')


def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


@app.route('/audiofeed')
def audiofeed():
    def gen(microphone):
        while True:
            sound = microphone.getSound()
            #with open('tmp.wav', 'rb') as myfile:
            #   yield myfile.read()

            yield sound

    return Response(stream_with_context(gen(Microphone())))


if __name__ == '__main__':
    app.config.from_object('config.Production.ProductionConfig')
    app.run()
