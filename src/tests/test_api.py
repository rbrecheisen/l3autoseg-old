from utils import get_token


def test_user_can_get_token():
    token = get_token('ralph', 'arturo4ever')
    print(token)
