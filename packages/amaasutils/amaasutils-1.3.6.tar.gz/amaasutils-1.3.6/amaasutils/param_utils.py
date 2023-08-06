from datetime import date, datetime
from dateutil.parser import parse


def param_to_array(param_name, search_params, value_type=str):
    if search_params is None:
        return None
    raw_param = search_params.get(param_name)
    values = raw_param.split(",") if raw_param else []
    if value_type in [int, str]:
        return [value_type(value) for value in values]
    elif value_type == bool:
        return [str_to_bool(value) for value in values]
    elif value_type in [date, datetime]:
        datetimes = [parse(value) for value in values]
        return [value.date() for value in datetimes] if value_type == date else datetimes


def param_to_boolean(param_name, search_params, default=None):
    if search_params is None:
        return default
    param = search_params.get(param_name, None)
    if param is None:
        return default
    return str_to_bool(param)


def str_to_bool(param):
    if param is None:
        return None
    if param.upper() == 'TRUE':
        return True
    if param.upper() == 'FALSE':
        return False


def param_to_datetime(param_name, search_params, date_only=False):
    if search_params is None:
        return None
    param = search_params.get(param_name)
    param = parse(param) if param else None
    if param and date_only:
        param = param.date()
    return param
