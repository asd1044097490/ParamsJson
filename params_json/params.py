from typing import List, Dict

PARAMS_DEFAULT_FORMAT = '_default_params_'


class ParamsBase:

    def __init__(self, many=False, many_number=1,
                 required=True, null=False, blank=False, **kwargs):
        self.params_many_number = many_number
        self.params_many = many
        self.params_blank = blank
        self.params_required = required
        self.params_null = null
        self.params_default = kwargs.pop('default', PARAMS_DEFAULT_FORMAT)


class Field(ParamsBase):
    pass


class CharField(Field):
    pass


class IntField(Field):
    pass


class Params(ParamsBase):

    def __init__(self, content=None, **kwargs):
        super().__init__(**kwargs)
        self.params_content = content

        if content is not None:
            assert isinstance(content, dict), '需要修改内容 key：content的类型必须是dict!'

        self.fields_dict = to_instance(self)


def __attrs(cls: object) -> dict:
    return cls.__class__.__dict__


def _to_data(cls: Params, data):
    """
    根据是否为列表返回内容
    :param cls:
    :param data:
    :return:
    """
    if is_many(cls):
        return [data for _ in range(cls.params_many_number)]
    return data


def is_many(cls: Params) -> bool:
    return cls.params_many


def is_modify(cls, default=PARAMS_DEFAULT_FORMAT):
    return cls.params_default != default


def is_all_modify(cls) -> List[str]:
    errors_msg = []
    error_format = '%s is not modify!'
    for key, params in to_instance(cls).items():
        if isinstance(params, Params):
            _errors_msg = [_ for _ in is_all_modify(params)]
            if _errors_msg:
                errors_msg.extend([key + '.' + msg for msg in _errors_msg])
        else:
            if not is_modify(params):
                errors_msg.append(error_format % (key))
    return errors_msg


__instance_typing = Dict[str, ParamsBase or Params]


def to_instance(cls: Params) -> __instance_typing:
    _dict = {}
    for key, value in __attrs(cls).items():
        if isinstance(value, ParamsBase):
            _dict[key] = value
    return _dict


def to_class(data: dict, cls: Params, *, is_default=False) -> Params:
    for key, value in data.items():
        if hasattr(cls, key):
            h = getattr(cls, key)
            # todo 列表没有处理
            if isinstance(h, Params) and isinstance(value, dict):
                setattr(cls, key, to_class(value, h, is_default=is_default))
            elif isinstance(cls, ParamsBase):
                h.params_default = value
                setattr(cls, key, h)
            else:
                raise TypeError(f'key: {key} class:{cls} type error!')
    return cls


def to_python(cls: Params, *, content=None, is_default=False):
    """

    :param cls:
    :param content:
    :param is_default:
    :return:
    """
    _dict = {}
    if is_default:
        if not isinstance(content, dict):
            content = {}
        if cls.params_content is not None:
            content.update(**cls.params_content)
    else:
        content = {}

    for key, params in to_instance(cls).items():
        if isinstance(params, Params):
            if key in content:
                _content = content.get(key)
                # 只满足更新当前类下的列表（整个替换,并不会单独的更新里面的内容）
                # todo 缺少更新向下递归的列表, {'family': [{'name': 'value1'}, {'name': 'value2'}...]} 暂时不满足这种方式的更新
                assert isinstance(_content, dict), f'列表不会自动向下更新！ key: {key}'
                _dict[key] = to_python(params, content=_content, is_default=is_default)
            else:
                _dict[key] = to_python(params, is_default=is_default)
        else:
            if key in content:
                _dict[key] = content[key]
            else:
                # 更新参数最后的值
                _dict[key] = _to_data(params, params.params_default)
    # 返回整个解析的内容
    return _to_data(cls, _dict)
