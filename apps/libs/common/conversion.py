from flask.json import dumps, loads

from apps.exception.error_code import ParameterException


def str_underline_to_hump(src: str, first_upper: bool = False):
    """
    将下划线分隔的名字,转换为驼峰模式
    :param src:
    :param first_upper: 转换后的首字母是否大写
    :return:
    """
    arr = src.split('_')
    res = ''
    for i in arr:
        res = res + i[0].upper() + i[1:]

    if not first_upper:
        res = res[0].lower() + res[1:]

    return res


def str_hump_to_underline(src: str):
    """
    将驼峰形式的名字，转换为下划线分隔
    :param src:
    :return:
    """
    lst = []
    for index, char in enumerate(src):
        if char.isupper() and index != 0:
            lst.append("_")
        lst.append(char)
    result = "".join(lst).lower()
    return result


def dict_underline_to_hump(src: dict, first_upper: bool = False):
    """
    将下划线分隔的名字,转换为驼峰模式
    :param src:
    :param first_upper: 转换后的首字母是否大写
    :return:
    """
    result = {}
    for key, value in src.items():
        arr = key.split('_')
        res = ''
        for i in arr:
            res = res + i[0].upper() + i[1:]

        if not first_upper:
            res = res[0].lower() + res[1:]

        result.update({res: value})
    return result


def dict_hump_to_underline(src: dict):
    """
    将驼峰形式的名字，转换为下划线分隔
    :param src:
    :return:
    """
    result = {}
    for key, value in src.items():
        lst = []
        for index, char in enumerate(key):
            if char.isupper() and index != 0:
                lst.append("_")
            lst.append(char)
        result.update({"".join(lst).lower(): value})
    return result


def recursion_underline_to_hump(data):
    if isinstance(data, dict):
        result = dict_underline_to_hump(data)
        for key, value in result.items():
            if isinstance(value, dict) or isinstance(value, list):
                result[key] = recursion_underline_to_hump(value)
            else:
                result[key] = value
        return result
    elif isinstance(data, list):
        result = []
        for item in data:
            if isinstance(item, dict):
                result.append(recursion_underline_to_hump(item))
            elif isinstance(item, list):
                raise ParameterException(msg='数据格式错误')
            elif isinstance(item, str) or isinstance(item, int):
                result.append(item)
            else:
                result.append(recursion_underline_to_hump(loads(dumps(item))))
        return result
    else:
        return data


def recursion_hump_to_underline(data):
    if isinstance(data, dict):
        result = dict_hump_to_underline(data)
        for key, value in result.items():
            if isinstance(value, dict) or isinstance(value, list):
                result[key] = recursion_hump_to_underline(result[key])
            else:
                result[key] = value
        return result
    elif isinstance(data, list):
        result = []
        for item in data:
            if isinstance(item, dict):
                result.append(recursion_hump_to_underline(item))
            elif isinstance(item, list):
                raise ParameterException(msg='数据格式错误')
            else:
                result.append(item)
        return result
