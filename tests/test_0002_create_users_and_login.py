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


def create_user(user_data, check_status=True):
    response = requests.post(f'{BASE_URL}/users', data=user_data)
    if check_status:
        response.raise_for_status()
        assert response.json() == {"message": "User created successfully"}
    return response


def get_users(check_status=True):
    response = requests.get(f'{BASE_URL}/users')
    if check_status:
        response.raise_for_status()
    return response


def get_num_users():
    return len(get_users().json()['users'])


def login(email, password, check_status=True):
    response = requests.post(f'{BASE_URL}/users/login', data={'email': email, 'password': password})
    if check_status:
        response.raise_for_status()
        assert response.json()['message'] == 'Login succeeded!'
        assert 'access_token' in response.json()
    return response


def test_0002_create_user():
    assert get_num_users() == 0

    response = create_user(USER_DATA_1)
    assert get_num_users() == 1

    response = create_user(USER_DATA_2)
    assert get_num_users() == 2

    response = create_user(USER_DATA_1, check_status=False)
    assert response.status_code == 409
    assert response.json() == {'message': 'User with this email already exists'}
    assert get_num_users() == 2

    login(USER_DATA_1['email'], USER_DATA_1['password'])
