import copy

from params_json.fields import Field


class FieldsMetaClass(type):
    def __new__(cls, name, bases, attrs: dict):
        current_fields = []
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
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


class BaseForm(metaclass=FieldsMetaClass):

    def __init__(self, data=None) -> None:
        self.data = data

        self.fields = copy.deepcopy(self.base_fields)

        self.errors = None

    def changed_data(self):
        """
        docstring
        """
        data = []
        for name, field in self.fields.items():
            pass


class Form(BaseForm, metaclass=FieldsMetaClass):
    pass
