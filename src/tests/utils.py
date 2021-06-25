import os
import requests


HOST = os.environ.get('L3AUTOSEG_HOST', 'http://localhost')
PORT = os.environ.get('L3AUTOSEG_PORT', 8002)
USER = os.environ.get('L3AUTOSEG_USER', None)
PASS = os.environ.get('L3AUTOSEG_PASSWORD', None)


def get_token(username=None, password=None):
    if username is None:
        username = USER
    if password is None:
        password = PASS
    result = requests.post(
        '{}:{}/token-requests/'.format(HOST, PORT), data={'username': username, 'password': password})
    assert result.status_code == 200, 'ERROR: {} ({})'.format(result.status_code, result.reason)
    return result.json()['token']


def get(endpoint, token, raw_result=False):
    result = requests.get(
        '{}:{}/{}'.format(HOST, PORT, endpoint), headers={'Authorization': 'Token {}'.format(token)})
    if raw_result:
        return result, result.status_code
    else:
        return result.json(), result.status_code


def get_binary(endpoint, token):
    result = requests.get(
        '{}:{}/{}'.format(HOST, PORT, endpoint), headers={'Authorization': 'Token {}'.format(token)})
    if result.status_code != 200:
        return result.json(), result.status_code
    else:
        return result.content, result.status_code


def post_json(endpoint, token, json, raw_result=False):
    result = requests.post(
        '{}:{}/{}'.format(HOST, PORT, endpoint), json=json,
        headers={
            'Authorization': 'Token {}'.format(token),
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
    )
    if raw_result:
        return result, result.status_code
    else:
        return result.json(), result.status_code


def post_files(endpoint, token, files, raw_result=False):
    result = requests.post(
        '{}:{}/{}'.format(HOST, PORT, endpoint), files=files, headers={'Authorization': 'Token {}'.format(token)})
    if raw_result:
        return result, result.status_code
    else:
        return result.json(), result.status_code


def delete(endpoint, token):
    result = requests.delete(
        '{}:{}/{}'.format(HOST, PORT, endpoint), headers={'Authorization': 'Token {}'.format(token)})
    return result, result.status_code
