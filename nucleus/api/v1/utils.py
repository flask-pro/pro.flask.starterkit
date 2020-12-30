from datetime import datetime
from typing import Any

from flask import abort
from werkzeug.datastructures import ImmutableMultiDict

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def args_to_dict(data: ImmutableMultiDict) -> dict:
    """Из объекта аргументов извлекаются повторяющиеся ключи,
    их значения объединяются в список и присваиваются ключу с общим именем.
    Если ключ не повторяется, он оставляется без изменений."""
    arguments = {}
    keys = data.keys()
    for key in keys:
        value = data.getlist(key)
        if len(value) > 1:
            arguments.update({key: data.getlist(key)})
        elif len(value) == 1:
            arguments.update({key: data[key]})
    return arguments


def check_to_equality(value: Any, field_name: str, parameters: dict) -> bool:
    if value != parameters[field_name]:
        abort(400, f"{field_name} from path does not match {field_name} from body request.")
    return True


def args_to_datetime(original_dict: dict, keys: list) -> dict:
    """В исходном словаре определённые ключи преобразуются в объекты datetime."""
    for key in keys:
        if key in original_dict:
            try:
                original_dict[key] = datetime.strptime(original_dict[key], DATETIME_FORMAT)
            except ValueError:
                abort(
                    400,
                    f"Value <{original_dict[key]}> from key <{key}>, is not valid datetime format.",
                )

    return original_dict
