# import copy
# from serializers.check import SerializerCheck
# from typing import Dict, List
# from serializers.fields import FieldBase, ObjectBase


# class SerializerBase:
#     def __init__(
#             self, name=None, data=None,
#             skip_serializer=False, skip_all=False,
#             required=True, null=False, empty=False, many=False) -> None:
#         """[summary]

#         Args:
#             name ([type], optional): [description]. Defaults to None.
#             skip_serializer (bool, optional): [description]. Defaults to False.
#             skip_all (bool, optional): [description]. Defaults to False.
#             required (bool, optional): [description]. Defaults to True.
#             null (bool, optional): [description]. Defaults to False.
#             empty (bool, optional): [description]. Defaults to False.
#         """
#         self.data = data

#         self.name = name
#         self.skip_serializer = skip_serializer
#         self.skip_all = skip_all

#         self.required = required
#         self.null = null
#         self.empty = empty
#         self.many = many

#         self.fields: Dict[str, FieldBase] = copy.deepcopy(self.base_fields)
#         self.error_dict = {}
#         self.is_init_data = False

#         self.check = SerializerCheck()

#     def init_data(self):
#         if self.many:
#             pass
#         else:
#             pass
        
#         for key, value in self.data:
#             pass

#         self.is_init_data = True

#     def run_check(self):
#         self.check.run_check(self)

#     # def init_data(self):
#     #     fields = copy.deepcopy(self.fields)
        
#     #     for name, field in fields.items():
#     #         field.name = name
#     #         field.default = self._data.get(name)
            

#     # @staticmethod
#     # def serializer_to_field(instance) -> ObjectBase:
#     #     """
#     #     serializer 转 objectBase

#     #     Args:
#     #         instance (SerialzerBase))

#     #     Returns:
#     #         ObjectBase
#     #     """
#     #     serializer: SerializerBase = instance

#     #     obj = ObjectBase(
#     #         required=serializer.required, 
#     #         null=serializer.null, 
#     #         empty=serializer.empty,
#     #         skip=serializer.skip_serializer,
#     #         skip_all=serializer.skip_all
#     #         )

#     #     return obj


# class SerializerMetaClass(type):
#     def __new__(cls, name, bases, attrs: dict):
#         current_fields = []

#         for key, value in list(attrs.items()):
#             # if isinstance(value, SerializerBase):
#             #     value = value.serializer_to_field(value)
            
#             # if isinstance(value, FieldBase):
#             if isinstance(value, (FieldBase, SerializerBase, )):
#                 value.name = key
#                 current_fields.append((key, value))
#                 attrs.pop(key)

#         attrs['declared_fields'] = dict(current_fields)

#         new_class = super().__new__(cls, name, bases, attrs)

#         declared_fields = {}

#         for base in reversed(new_class.__mro__):
#             # Collect fields from base class.
#             if hasattr(base, 'declared_fields'):
#                 declared_fields.update(base.declared_fields)

#             # Field shadowing.
#             for attr, value in base.__dict__.items():
#                 if value is None and attr in declared_fields:
#                     declared_fields.pop(attr)

#         new_class.base_fields = declared_fields
#         new_class.declared_fields = declared_fields

#         return new_class


# class Serializer(SerializerBase, metaclass=SerializerMetaClass):
#     pass

#     # def __init__(self, name, skip_serializer, skip_all, required, null, empty) -> None:
#     #     super().__init__(name=name, skip_serializer=skip_serializer,
#     #                      skip_all=skip_all, required=required, null=null, empty=empty)

#     #     self.fields = copy.deepcopy(self.base_fields)
