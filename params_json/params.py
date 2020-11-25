from params_json.errors import ParamsTypeError, CheckError

DEFAULT_VALUE = 'default_value'

# KEY
REQUIRED = '__required'
MAX_LENGTH = '__max_length'


def __get(data: dict, key, default=DEFAULT_VALUE):
    return data.get(key, default)


def _get_max_length(data):
    return __get(data, MAX_LENGTH)


def _get_required(data):
    return __get(data, REQUIRED)


def _is_back_check(config):
    """
    判断是否需要后续的测试
    1.如果是非必填的情况下,并且内容为 默认值 DEFAULT_VALUE
    2.如果是必填字段,但是默认值是 DEFAULT_VALUE
    3.如果校验 required 没有通过,那么不需要后续的校验
    :param config:
    :return:
    """


def check_required(data, config: dict) -> CheckError or None:
    _required = _get_required(config)
    if not isinstance(_required, bool):
        raise ParamsTypeError(f'{REQUIRED} type is bool!')
    # required 为 false 不需要校验
    if _required:
        if data == DEFAULT_VALUE:
            return CheckError('')


def to_config_base(required: bool = True, null: bool = False, blank: bool = False, many: bool = False):
    return {
        '__required': required,
        '__null': null,
        '__blank': blank,
        '__many': many,
        # '__check': ['check_required', 'check_null', 'check_blank']
        '__check': [check_required]
    }


def to_choices_config(choices: list = None):
    return {
        '__choices': choices,
    }


def to_char_config(max_length: int = None, min_length: int = None, length: int = None, choices: list = None,
                   required: bool = True, null: bool = False, blank: bool = False):
    if length is None and min_length is None:
        min_length = 0
    config = {
        '__max_length': max_length,
        '__min_length': min_length,
        '__length': length,
        **to_config_base(required=required, null=null, blank=blank),
        **to_choices_config(choices=choices),
        # '__check': ['check_max_length', 'check_min_length', 'check_length', 'check_choices']
        '__check': [check_required]
    }
    return config


def to_integer_config(
        max_value: int = None, min_value: int = None, choices: list = None,
        required: bool = True, null: bool = False, blank: bool = False):
    pass


def to_config(
        target: dict = None, many: bool = False,
        max_length: int = None, min_length: int = None, length: int = None,
        required: bool = True, null: bool = False, blank: bool = False):
    """

    :param many:
    :param target: 列表中的对象,可以是dict, str, int, float...
    :param max_length:
    :param min_length:
    :param length:
    :param required:
    :param null:
    :param blank:
    :return:
    """
    if length is None and min_length is None:
        min_length = 0
    config = {
        '__max_length': max_length,
        '__min_length': min_length,
        '__length': length,
        **to_config_base(required=required, null=null, blank=blank, many=many),
        **target,
    }
    return config


def _add_error(errors: list, error):
    if isinstance(error, CheckError):
        errors.append(error)
    return errors


def _is_check_error(error):
    return isinstance(error, CheckError)


def check_dict(data: dict, config: dict) -> list:
    errors = []
    for key, value_c in config.items():
        # assert key is exist
        value_d = __get(data, key)
        error = check_required(value_d, value_c)
        # 如果返回结果是 CheckError 的子类,那么不需要后续要的校验, 如果是 CheckError 说明该字段在数据中不存在
        _add_error(errors, error)
        if _is_check_error(error):
            continue
    return errors


family = {
    'name': to_char_config(max_length=10),
    'age': to_char_config(),
}

data = {
    'name': to_char_config(max_length=10),
    'family': to_config(many=True, target=family)
}

data1 = {
}

errors = check_dict(data1, data)
print(errors)
