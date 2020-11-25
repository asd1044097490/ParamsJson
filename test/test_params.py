import unittest

from params_json import Params, CharField, IntField, to_python
from params_json.params import PARAMS_DEFAULT_FORMAT, to_class


class Base(unittest.TestCase):
    def setUp(self) -> None:
        class NotDefaultCustom(Params):
            name = CharField()
            age = IntField()
            sex = IntField()

        class DefaultCustom(Params):
            name = CharField(default='gaga')
            age = IntField(default=10)
            sex = IntField(default=1)

        class NotDefaultFamilyDict(Params):
            family = NotDefaultCustom()
            count = IntField()

        class NotDefaultFamilyList(Params):
            family = NotDefaultCustom(many=True)
            count = IntField()

        class DefaultFamilyList(Params):
            family = DefaultCustom(many=True)
            count = IntField()

        class DefaultFamilyDict(Params):
            family = DefaultCustom()
            count = IntField(default=5)

        self.default_custom = DefaultCustom
        self.not_default_custom = NotDefaultCustom
        self.default_family_list = DefaultFamilyList
        self.default_family_dict = DefaultFamilyDict
        self.not_default_family_list = NotDefaultFamilyList
        self.not_default_family_dict = NotDefaultFamilyDict

    def test_single_default_to_python(self):
        """有默认值的class to python """
        custom = self.default_custom()
        data = to_python(custom)
        self.assertEqual(data, {'name': 'gaga', 'age': 10, 'sex': 1})

    def test_single_not_default_to_python(self):
        """没有默认真class to python"""
        custom = self.not_default_custom()
        data = to_python(custom)
        self.assertEqual(data, {'name': PARAMS_DEFAULT_FORMAT, 'age': PARAMS_DEFAULT_FORMAT, 'sex': PARAMS_DEFAULT_FORMAT})

    def test_single_to_python_init(self):
        """有默认值，to python 使用初始化"""
        custom = self.default_custom()
        data = to_python(custom, is_init=True)
        self.assertEqual(data, {'name': PARAMS_DEFAULT_FORMAT, 'age': PARAMS_DEFAULT_FORMAT, 'sex': PARAMS_DEFAULT_FORMAT})

    def test_single_to_python_not_init(self):
        """有默认值，to python 不使用初始化"""
        custom = self.default_custom()
        data = to_python(custom, is_init=False)
        self.assertEqual(data, {'name': 'gaga', 'age': 10, 'sex': 1})

    def test_single_default_to_class_init(self):
        """无嵌套 to class 使用初始化"""
        data = {'name': 'gaga', 'age': 10, 'sex': 1}
        cls = to_class(data, self.default_custom())
        self.assertEqual(to_python(cls), data)
