import pytest
import json
from flask import g, session, jsonify

def test_cli_login(client, auth):
    assert client.get('/auth/cli/login').status_code == 200
    response = auth.login_cli()

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

json = {}
json['id'] = 1
json['name'] = 'test'
json['skills'] = 'something'

@pytest.mark.parametrize(('data', 'message'), (
    (json, b'Vacany post successful'),
    ({}, b'Vacancy post unsuccessful'),
))
def test_post_vacancy(client, jobs, data, message):
    response = jobs.post_vacancy(data)
    assert message in response.data

json = {}
json['id'] = 1
json['name'] = 'applicant'
json['skills'] = 'something'

@pytest.mark.parametrize(('data', 'message'), (
    (json, b'Application post successful'),
    ({}, b'Application post unsuccessful'),
))
def test_post_application(client, jobs, data, message):
    response = jobs.apply_to_vacancy(data)
    assert message in response.data

json = {}
json['id'] = 1

def test_get_vacancies(client, jobs):
    response = jobs.get_vacancies(json)
    assert 'test' in response

def test_get_vacancies(client, jobs):
    response = jobs.retrieve_application(json)
    assert 'applicant' in response
