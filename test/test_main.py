import pytest
import project
import random
import string


def id_generator(size=7, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@pytest.fixture
def client():
    project.app.config.from_object('config.Testing.TestingConfig')
    client =  project.app.test_client()
    with project.app.app_context():
        project.init_db()
    yield client


def test_register(client):
    username = id_generator()
    password = id_generator()
    type_of_user = 'Normal'
    email = id_generator()+'@'+id_generator()
    rv = client.post('/handle_data', data=dict(
        Register_New_User=username,
        Register_New_Password=password,
        permissions=type_of_user,
        Email=email,
        type_form='register'
    ), follow_redirects=True)
    rv = client.post('/logout', follow_redirects=True)
    userTemp = project.User.query.filter_by(username=username).first()
    project.user_datastore.delete_user(userTemp)
    project.db_session.commit()
    assert b'Log In' not in rv.data


def test_login(client):
    username = id_generator()
    password = id_generator()
    type_of_user = 'Normal'
    email = id_generator()+'@'+id_generator()
    rv = client.post('/handle_data', data=dict(
        Register_New_User=username,
        Register_New_Password=password,
        permissions=type_of_user,
        Email=email,
        type_form='register'
    ), follow_redirects=True)

    rv = client.post('/logout', follow_redirects=True)
    print(rv.data)
    rv = client.post('/handle_data', data=dict(
        inputIdMain=username,
        inputPasswordMain=password,
        type_form='login'
    ), follow_redirects=True)
    assert b'Log In' in rv.data


