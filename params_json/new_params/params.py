from params_json.new_params.check_mixin import CheckMixin, CheckParamsMixin


class ParamsBase(CheckMixin):
    """
    1.框架本身是不存在default字段的,
    """

    _default_value = 'default'

    def is_fields(self):
        # 区分field与dict、list
        return True

    def is_params_list(self):
        return False

    def is_current_params(self):
        if self._name is None:
            return True
        return False

    def is_default_value_changed(self) -> bool:
        """
        判断内容是否改变
        True: yes
        False: no
        """
        if self.params_value != self._default_value:
            return True
        return False

    def __init__(self, *, name=None,
                 many=False, many_number=None,
                 null=False, blank=False, required=True, **kwargs):
        """

        :param default:
        :param name:
        :param null: True 可以为null
        :param blank: 同上
        :param required: 同上
        """
        self._required = required
        self._blank = blank
        self._null = null
        self._name = name

        self._default = kwargs.pop(self._default_value, self._default_value)
        # 父级obj
        # 追寻上级
        self._parent = None

        self._fields_traceback_list = []
        self._errors = []

        self._many_number = many_number
        self._many = many
        if self._many and self._many_number is None:
            self._many_number = 1

    def _traceback(self, obj):
        """
        追寻上级
        :param obj:
        :return:
        """
        # 如果存在值说明该field已经回溯过一次了
        if self._fields_traceback_list:
            self._fields_traceback_list.clear()
        _parent: ParamsBase = obj
        while _parent:
            self._fields_traceback_list.insert(0, _parent._name)
            _parent = _parent._parent
        return self._fields_traceback_list

    def params_is_valid(self):
        self.params_check()
        if self._errors:
            return False
        return True

    @property
    def _params_errors(self):
        """错误详情,是一个列表"""
        return self._errors

    @property
    def params_errors(self):
        if self._params_errors:
            return self._params_errors[0]
        else:
            return self._params_errors

    @property
    def params_traceback(self):
        return self._fields_traceback_list

    @property
    def traceback_format(self):
        return '.'.join([_ for _ in self._fields_traceback_list[1:]])

    @property
    def params_value(self):
        """返回默认值"""
        return self._default


class FieldsParamsBase(ParamsBase):
    pass


class Params(CheckParamsMixin, ParamsBase):

    class Meta:
        # None 说明并没有设置, 只要改变了，那么将会遵守此配置,会覆盖个体配置
        global_blank = None
        global_null = None
        global_required = None

    def is_fields(self):
        return False

    def is_params_list(self):
        return self._many

    def __new__(cls, *args, **kwargs):
        fields = []
        fields_dict_instance = {}

        for key, params in cls.__dict__.items():
            if not key.startswith('_') and not key.endswith('_') and isinstance(params, ParamsBase):
                params._name = key
                fields.append(key)
                fields_dict_instance[key] = params

        cls.fields = fields
        cls.fields_dict_instance = fields_dict_instance

        cls.args = args
        cls.kwargs = kwargs
        return super().__new__(cls)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.params_data = {}

    @property
    def params_value(self):
        """
        返回默认值，如果是一个Params类型的数据进行额外处理
        在Params中又分为了单个Params和多个Params 即 list 和 dict
        """
        if self.is_params_list():
            return self._value_params_list()
        else:
            return self._value_params()

    @property
    def params_values_dict(self):
        if self.is_params_list():
            return {self._name: self._value_params_list()}

    def _value_call_black(self, key, params):
        params._parent = self
        self.params_data[key] = params.params_value

    def _fields_dict_instance_items(self, call_black):
        """
        :param call_black: 主回调函数
        """
        for key, params in self.fields_dict_instance.items():
            call_black(key, params)

    def _value_params(self):
        # 处理Params类型的数据
        self._fields_dict_instance_items(self._value_call_black)
        return self.params_data

    def _value_params_list(self):
        # 处理 [Params]类型数据
        return [self._value_params() for _ in range(self._many_number)]


class CharField(FieldsParamsBase):
    pass


class CustomParams(Params):
    name = CharField()
    age = CharField(default=None)


class FamilyParams(Params):
    family = CustomParams(many=True)
    count = CharField(default=None, blank=True, null=True)


if __name__ == '__main__':
    m_params = FamilyParams()
    print(m_params.params_value)
    print(m_params.params_is_valid())
    print(m_params.params_errors)
