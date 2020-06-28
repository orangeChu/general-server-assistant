from secrets import token_urlsafe

from app.tools.db_tools import get_collection
from app.tools.sha1_tools import sha1_encode


def login(user_info):
    """
        user login
    :param user_info: dict user info
    :return: dict user info
    """
    user_info = get_user(user_info.get('name'), user_info.get('password'))
    if user_info is not None:
        user_info.pop("_id")
        return user_info
    return None


def get_user(name, password):
    """
        get user by name and password
    :param name: user name
    :param password: password
    :return: user info
    """
    collection = get_collection("user")
    user_info = collection.find_one({"name": name, "password": get_password(name, password)})
    return user_info


def get_user_by_token(token):
    """
        use plugin token to get use info
    :param token: plugin token
    :return: user info
    """
    collection = get_collection("user")
    user_info = collection.find_one({"token": token})
    return user_info


def update(user_info):
    """
        update user info in database
    :param user_info: dict user info
    :return:
    """
    collection = get_collection("user")
    collection.update({"name": user_info['name']}, user_info)


def update_password(user_info):
    """
        update password
    :param user_info:
    :return:
    """
    collection = get_collection("user")
    if user_info.get('password') and user_info.get('password') != '':
        user_info['password'] = get_password(user_info['name'], user_info['password'])
    collection.update({"name": user_info['name']}, user_info)


def get_password(user_name, password):
    return sha1_encode(user_name + password)


def generate_token(user):
    """
        save plugin token
    :return: token
    """
    token = token_urlsafe(16)
    user['token'] = token
    update(user)
    return token
