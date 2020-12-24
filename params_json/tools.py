import copy


DEFAULT_FORMAT = '_Params_Default_'


class Cls:
    pass


class ValueBase:
    default_format = DEFAULT_FORMAT

    def __init__(self, many, value) -> None:
        self.many = many
        self.value = value

    def to_list_data(self): 
        if self.many:
            return 


class Field:

    def __init__(self, many=False, required=True, name=None, default=DEFAULT_FORMAT) -> None:
        self.required = required
        self.name = name
        self.default = default
        self.many = many

        self.value_instance = ValueBase(many=self.many, value=self.default)

    def to_value(self):
        """
        docstring
        """
        return self.default


class Params(Field):

    def __init__(self, data=None, **kwargs) -> None:
        super().__init__(**kwargs)

        self.is_init: bool = False  # 是否初始化完成
        self.params_fields_list = []
        self.params_dict = {}

        self._data = data

    def init(self):
        """
        初始化
        """
        for key, obj in self.__class__.__dict__.items():
            if isinstance(obj, Field):
                self.params_fields_list.append(key)
                obj.name = key

                self.params_dict[key] = obj

        self.is_init = True

    def _is_init(self):
        """
        初始化
        """
        if not self.is_init:
            self.init()

    def to_dict_instance(self):
        """
        to dict
        """
        self._is_init()
        return self.params_dict

    def to_value(self):
        """
        to value
        """
        self._is_init()

        value_dict = {}

        for key, field in self.params_dict.items():
            value_dict[key] = field.to_value()

        return value_dict

    def to_cls(self):
        """
        to class
        """
        if not self._data:
            raise ValueError('data error!')

        copy.deepcopy(self)

        for key, field in self.params_dict.items():
            pass


class Custom(Params):
    name = Field()
    age = Field()


class Family(Params):
    family = Custom()
    count = Field()


if __name__ == "__main__":
    test = Family()
    print(test.to_dict_instance())
    print(test.to_value())
