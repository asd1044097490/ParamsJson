from params_json.new_params.erros import CheckError


class CheckMixin:
    """
    当 required 和 其他的校验检查冲突的时候
    例1：required is False 遵循以下规则：
    1.当当前的key不存在的时候，即self.params_value = 'default',
    会认为该值是不存在的，是找不到该key，虽然实际上可以找到，但是并没有手动的去更新该key对应的value,所以认为它是找不到的
    2.如果该key为非必填,但是框架却判断到了该值经过了修改,
    那么会认为required 为 True 依然会进行规则检查校验,params_is_valid 为True或False
    # 例2：null is True, 该字段本身是可以为None的，但是获取到了该字段的值，那么依然会进行检查校验

    全局检查校验
    如果在Meta中配置了global_null,global_blank,global_required......配置Meta校验的当前类下所有的field将遵循Meta中的配置

    """

    default_check_list = ['check_required', 'check_null', 'check_blank', ]

    @staticmethod
    def _is_check_global(condition1, condition2) -> bool:
        """
        判断是遵循全局检查校验还是field中配置的
        :param condition1: ParamsBase.Meta.global... type: bool
        :param condition2: ParamsBase._null,ParamsBase._blank,ParamsBase._required...... type: bool
        :return:
        """
        # 判断Meta中的相关检查校验配置是否发生更改,默认是一个None
        if condition1 is not None and isinstance(condition1, bool):
            return condition1
        # blank True 不校验，False 校验
        # null True 不校验，False 校验
        # required True 校验，False 不校验
        if not condition2:
            return True
        return False

    def is_check_blank(self) -> bool:
        return self._is_check_global(self._parent.Meta.global_blank, self._blank)

    def is_check_null(self):
        return self._is_check_global(self._parent.Meta.global_null, self._null)

    def is_check_required(self):
        # required True 校验，False 不校验
        return self._is_check_global(not self._parent.Meta.global_required, not self._required)

    def is_back_check(self) -> bool:
        """
        是否需要后续的检查校验
        主要解决required与其他校验规则的冲突
        例：当配置一个field为required is False self._required = False 那么说明这个字段是非必填字段
        1.虽然这个字段是非必填字段,但是也有填写的情况
        这个字段发生了改变 self._default != self._default_value
        那么就需要检查这个字段中的内容
        2.如果没有没有发现改变那么不需要检查
        True 需要后续的校验检查
        False 不需要后续的校验检查
        """
        if self._parent.Meta.global_required is not None:
            if self._parent.Meta.global_required:
                return True
        elif self._required:
            return True
        else:
            return self.is_default_value_changed()

    def _error_format(self, msg):
        return CheckError(f'"{self.traceback_format}" {msg}')

    def get_default_check_list(self):
        return self.default_check_list

    def add_check_func(self):
        for key, fields in self.fields_dict_instance.items():
            _check_name = 'check_' + key
            if hasattr(self, _check_name):
                self.get_default_check_list.append(_check_name)

    def params_check(self):
        # 需不需要后续的检查
        if not self.is_back_check():
            return
        for func_check_name in self.get_default_check_list():
            if hasattr(self, func_check_name):
                check_func = getattr(self, func_check_name)
                check_result = check_func()
                if isinstance(check_result, CheckError):
                    self._errors.append(check_result)
        return self.params_value

    def check_null(self):
        if not self._null:
            if self.params_value is None:
                self._traceback(self)
                # return CheckError(f'"{self.traceback_format}" is not None!')
                return self._error_format(msg='is not None!')
        return self.params_value

    def check_required(self):
        if self._required:
            if self.params_value == self._default_value:
                self._traceback(self)
                # return CheckError(f'"{self.traceback_format}" is required!')
                return self._error_format(msg='is required!')
        return self.params_value

    def check_blank(self):
        if not self._blank:
            if self.params_value == '':
                self._traceback(self)
                # return CheckError(f'"{self.traceback_format}" is not blank!')
                return self._error_format(msg='is not blank!')


class CheckParamsMixin(CheckMixin):

    def params_check(self):
        error_dict = {}
        # 如果是当前的Params那么是不需要校验的
        if not self.is_current_params():
            super(CheckParamsMixin, self).params_check()

        def check_params_call_black(key, params):
            if isinstance(params, self.__class__):
                params.add_check_func()

            if not params.params_is_valid():
                error_dict[key] = params._params_errors

        self._fields_dict_instance_items(check_params_call_black)

        if error_dict:
            self._errors.append(error_dict)

    def check_blank(self):
        # if self.is_params_list:
        if not self._blank:
            if self.is_params_list:
                if not isinstance(self.params_value, list):
                    self._traceback(self)
                    return self._error_format(msg='is list!')
            else:
                if not isinstance(self.params_value, dict):
                    self._traceback(self)
                    return self._error_format(msg='is dict!')

    def check_required(self):
        return super(CheckParamsMixin, self).check_required()

    def check_null(self):
        return super(CheckParamsMixin, self).check_null()
