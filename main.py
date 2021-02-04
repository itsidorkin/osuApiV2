import json
import requests
import webbrowser
from pyperclip import paste, copy
from time import sleep


def auth(personal_data, token_exists):
    if token_exists:                                    # аксес устарел
        grant_type = 'refresh_token'
        code = 'refresh_token'
    else:                                               # аксеса нет
        grant_type = 'authorization_code'
        code = 'code'
    params = {
        'client_id': personal_data['client_id'],
        'client_secret': personal_data['client_secret'],
        'grant_type': grant_type,
        'redirect_url': personal_data['redirect_url'],
        code: personal_data['code']
    }
    return requests.post('https://osu.ppy.sh/oauth/token', data=params).json()


def rooms_data(token):
    access_token = {
        'Authorization': 'Bearer {}'.format(token)
    }
    return requests.get('https://osu.ppy.sh/api/v2/rooms', headers=access_token).json()


def write_personal_data(personal_data):
    with open("personalData.json", "w") as j:
        json.dump(obj=personal_data, fp=j, indent=2)


def refresh_tokens(personal_data, token_exists):
    tokens = auth(personal_data, token_exists)
    personal_data['access'] = tokens['access_token']
    personal_data['code'] = tokens['refresh_token']
    write_personal_data(personal_data)
    return rooms_data(personal_data['access'])


def get_started(personal_data):
    url = 'https://osu.ppy.sh/oauth/authorize?client_id={}&redirect_url={}&response_type=code&scope=public'.format(
        personalData['client_id'], personalData['redirect_url'])
    webbrowser.open_new_tab(url)
    copy('')
    print('Ожидание code...')
    while paste().find('def') == -1 and len(paste()) < 512:  # не уверен может ли меняться длина code
        sleep(2)
    personal_data['code'] = paste()
    print('Code получен')
    copy('')
    write_personal_data(personal_data)
    return refresh_tokens(personalData, False)


with open("personalData.json") as i:
    personalData = json.load(i)


if personalData['access'] == "":  # аксес (соответсвенно и code) отсутствуют
    data = get_started(personalData)
else:
    data = rooms_data(personalData['access'])
    if len(data) == 1 and data['authentication'] == 'basic':  # аксес устарел ???
        data = refresh_tokens(personalData, True)
        if len(data) == 1 and data['authentication'] == 'basic':  # рефреш устарел ???
            data = get_started(personalData)

print(data)
