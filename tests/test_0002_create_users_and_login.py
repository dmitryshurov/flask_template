import requests

from .helpers import BASE_URL

USER_DATA_1 = {
    'first_name': 'Dmitry',
    'last_name': 'Shurov',
    'email': 'd.l.shurov@gmail.com',
    'password': '123456',
}


USER_DATA_2 = {
    'first_name': 'Dmitry',
    'last_name': 'Shurov',
    'email': 'dmitry.shurov@mail.ru',
    'password': '123456',
}

USER_DATA_3 = {'email': 'dmitry.shurov@mail.ru', 'password': '1234567'}
USER_DATA_4 = {'email': 'dmitry.shurov@mail.ru1', 'password': '123456'}
USER_DATA_5 = {'email': 'dmitry.shurov@mail.ru', 'password': ''}
USER_DATA_6 = {'email': '', 'password': ''}
USER_DATA_7 = {'email': ''}
USER_DATA_8 = {}


def create_user(user_data, check_status=True, json=True):
    if json:
        response = requests.post(f'{BASE_URL}/users', json=user_data)
    else:
        response = requests.post(f'{BASE_URL}/users', data=user_data)

    if check_status:
        response.raise_for_status()
        assert response.json() == {"message": "User created successfully"}
    return response


def login(user_data, check_status=True, json=True):
    login_user_data = {'email': user_data['email'], 'password': user_data['password']}

    if json:
        response = requests.post(f'{BASE_URL}/users/login', json=login_user_data)
    else:
        response = requests.post(f'{BASE_URL}/users/login', data=login_user_data)

    if check_status:
        response.raise_for_status()
        assert response.json()['message'] == 'Login succeeded!'
        assert 'access_token' in response.json()
    return response


def check_login_failed(user_data):
    response = login(user_data, check_status=False)
    assert response.status_code == 401
    assert response.json()['message'] == 'Bad email or password'


def get_users(check_status=True):
    response = requests.get(f'{BASE_URL}/users')
    if check_status:
        response.raise_for_status()
    return response


def get_num_users():
    return len(get_users().json()['users'])


def test_0002_create_user():
    assert get_num_users() == 0

    response = create_user(USER_DATA_1)
    assert get_num_users() == 1

    response = create_user(USER_DATA_2, json=True)
    assert get_num_users() == 2

    response = create_user(USER_DATA_1, check_status=False)
    assert response.status_code == 409
    assert response.json() == {'message': 'User with this email already exists'}
    assert get_num_users() == 2

    login(USER_DATA_1)
    login(USER_DATA_2, json=True)

    check_login_failed(USER_DATA_3)
    check_login_failed(USER_DATA_4)
    check_login_failed(USER_DATA_5)
    check_login_failed(USER_DATA_6)
    check_login_failed(USER_DATA_7)
    check_login_failed(USER_DATA_8)
