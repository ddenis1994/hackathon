import pytest
import project


@pytest.fixture
def client():
    project.app.config.from_object('config.Testing.TestingConfig')
    client =  project.app.test_client()
    with project.app.app_context():
        project.init_db()
    yield client


def test_register(client):
    username="test1"
    password="test1"
    type_of_user="manger"
    email="test1@test.co.il"
    rv=client.post('/handle_data', data=dict(
        Register_New_User=username,
        Register_New_Password=password,
        permissions=type_of_user,
        Email=email,
        type_form='register'
    ), follow_redirects=True)
    print(rv.data)
    assert b'Log In' in rv.data



