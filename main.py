import json
import webbrowser
from time import sleep

import requests
from pyperclip import paste, copy


def auth(personal_data, token_exists):
    if token_exists:  # аксес устарел
        grant_type = 'refresh_token'
        code = 'refresh_token'
    else:  # аксеса нет
        grant_type = 'authorization_code'
        code = 'code'
    params = {
        'client_id': personal_data['client_id'],
        'client_secret': personal_data['client_secret'],
        'grant_type': grant_type,
        'redirect_uri': personal_data['redirect_uri'],
        code: personal_data['code']
    }
    tokens = requests.post('https://osu.ppy.sh/oauth/token', data=params)
    if tokens.status_code == 401:  # рефреш устарел
        return get_started(personal_data, True)
    else:
        return tokens.json()


def rooms_data(token):
    access_token = {
        'Authorization': 'Bearer {}'.format(token)
    }
    return requests.get('https://osu.ppy.sh/api/v2/rooms', headers=access_token).json()


def write_personal_data(personal_data):
    with open("personalData.json", "w") as j:
        json.dump(obj=personal_data, fp=j, indent=2)


def refresh_tokens(personal_data, token_exists, token_dead):
    tokens = auth(personal_data, token_exists)
    if token_dead:
        return tokens
    personal_data['access'] = tokens['access_token']
    personal_data['code'] = tokens['refresh_token']
    write_personal_data(personal_data)
    return rooms_data(personal_data['access'])


def get_started(personal_data, token_dead):
    url = 'https://osu.ppy.sh/oauth/authorize?client_id={}&redirect_uri={}&response_type=code&scope=public'.format(
        personalData['client_id'], personalData['redirect_uri'])
    webbrowser.open_new_tab(url)
    copy('')
    print('Ожидание code...')
    while paste().find('def') == -1 or len(paste()) != 754:  # не уверен может ли меняться длина code
        sleep(2)
    personal_data['code'] = paste()
    print('Code получен')
    copy('')
    write_personal_data(personal_data)
    return refresh_tokens(personal_data, False, token_dead)


with open("personalData.json") as i:
    personalData = json.load(i)

if personalData['access'] == "":  # аксес (соответсвенно и code) отсутствуют
    data = get_started(personalData, False)
else:
    data = rooms_data(personalData['access'])
    if len(data) == 1 and data['authentication'] == 'basic':  # аксес (вероятно и code) устарел ???
        data = refresh_tokens(personalData, True, False)

print(data)
