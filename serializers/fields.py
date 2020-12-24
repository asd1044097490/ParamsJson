import copy
from typing import DefaultDict, Dict, Type
from serializers.check import Check, ObjectCheck


class FieldBase:

    special = (
        list, dict, 
    )
    not_special = (
        str, int, float, 
    )

    def __init__(
            self, name=None, data=None, many=False,
            skip=False, skip_all=False,
            required=True, null=False, empty=False, default=None, ) -> None:
        
        self.name = name
        self.required = required
        self.null = null
        self.empty = empty
        self.default = default
        self.many, self.many_data = many, None
        self.data = data

        self.skip, self.skip_all = skip, skip_all

        self.check: Check = Check()
        self.error_dict = {}

        self.is_init_data = False

    def run_check(self):
        return self.check.run_check(self)

    def init_data(self):
        pass


class ObjectBase(FieldBase):

    def __init__(
        self, name=None, data=None, many=False, 
        required=True, null=False, empty=False, 
        default=None) -> None:

        super().__init__(name=name, data=data, many=many,
                         required=required, null=null, empty=empty, default=default)

        self.fields: Dict[str, FieldBase] = copy.deepcopy(self.base_fields)
        self.error_dict = {}
        

        self.check = ObjectCheck()

    def init_data(self):
        if self.many:
            if not isinstance(self.data, list):
                raise TypeError('if many is True so type is list!')
            self.many_data = self.data
            
            # [{}, {}, {}, ...]
            for data in self.data:
                # 判断是否为 object
                # 在需要校验的时候进行修改和赋值
                if not isinstance(data, dict):
                    raise TypeError('this is dict!')
        else:
            for key, value in self.data.items():

                field = self.fields.get(key)
                field.data = value
                field.init_data()

                self.fields.update({key: field})

        self.is_init_data = True



class ObjectMetaClass(type):
    def __new__(cls, name, bases, attrs: dict):
        current_fields = []

        for key, value in list(attrs.items()):
            # if isinstance(value, SerializerBase):
            #     value = value.serializer_to_field(value)

            # if isinstance(value, FieldBase):
            if isinstance(value, (FieldBase, )):
                value.name = key
                current_fields.append((key, value))
                attrs.pop(key)

        attrs['declared_fields'] = dict(current_fields)

        new_class = super().__new__(cls, name, bases, attrs)

        declared_fields = {}

        for base in reversed(new_class.__mro__):
            # Collect fields from base class.
            if hasattr(base, 'declared_fields'):
                declared_fields.update(base.declared_fields)

            # Field shadowing.
            for attr, value in base.__dict__.items():
                if value is None and attr in declared_fields:
                    declared_fields.pop(attr)

        new_class.base_fields = declared_fields
        new_class.declared_fields = declared_fields

        return new_class


class Object(ObjectBase, metaclass=ObjectMetaClass):
    pass


class Field(FieldBase):
    
    def init_data(self):
        # 非对象和列表
        if self.many:
            if not isinstance(self.data, list):
                raise TypeError('many is True os type is list!')
            self.many_data = self.data

        self.is_init_data = True
