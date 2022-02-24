import os
from typing import List, Union, Dict
import random
import string  # define the random 


# def route_prefix(url_prefixName):
#     return f"{API_URL}/{url_prefixName}"


def random_str(size=7) -> str:
    ran = ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=size))
    return ran


def get_user_address(
        user_address: Union[List, Dict] = None) -> Union[List, Dict]:
    if isinstance(user_address, list) and len(user_address) > 0:
        user_address_obj = user_address[0]
        return user_address_obj
    elif isinstance(user_address, dict):
        user_address_obj = user_address
        return user_address_obj
    else:
        return None


def run_once(f):

    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)

    wrapper.has_run = False
    return wrapper


def get_base_dir():
    current_wdr = os.getcwd()
    if os.path.isdir(os.path.join(current_wdr, os.getcwd().split("\\")[-1])):
        return os.path.join(current_wdr, os.getcwd().split("\\")[-1])
    return os.getcwd()

