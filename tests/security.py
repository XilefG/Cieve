import pytest
from flask import g, session

# Client login tests

def test_cli_login(client, auth):
    assert client.get('/auth/cli/login').status_code == 200
    response = auth.login_cli()

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username or password.'),
    ('test', 'a', b'Incorrect username or password.'),
))
def test_cli_login_validate_input(auth, username, password, message):
    response = auth.login_cli(username, password)
    assert message in response.data

# Applicant login tests

def test_apl_login(client, auth):
    assert client.get('/auth/apl/login').status_code == 200
    response = auth.login_apl()

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username or password.'),
    ('test', 'a', b'Incorrect username or password.'),
))
def test_apl_login_validate_input(auth, username, password, message):
    response = auth.login_apl(username, password)
    assert message in response.data

# Applicant registration tests

def test_register(client, app):
    assert client.get('/auth/apl/register').status_code == 200
    response = client.post('/auth/apl/register', data={'username': 'a', 'password': 'a'})
    assert 'http://localhost/auth/apl/login' == response.headers['Location']

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'Username test is already taken.'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_pytest():
    assert 1 = 1