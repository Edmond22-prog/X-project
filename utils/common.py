import uuid
from typing import List, Tuple


def generate_uuid():
    """
    Generate a string uuid.
    :return:
    """
    return uuid.uuid4().hex


def build_tuple_types(enum_type: object) -> Tuple:
    """
    Map Enum to typle.

    :param enum_type:
    :return:
    """
    return tuple([(item.value, item.value) for item in enum_type])


def build_list_types(enum_type: object) -> List:
    """
    Map Enum to list.

    :param enum_type:
    :return:
    """
    return [item.value for item in enum_type]
