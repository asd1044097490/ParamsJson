import unittest

from params_json import Params, CharField, IntField, to_python


class TestToPythonBase(unittest.TestCase):
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
        print(2)


class TestToPythonSingle(TestToPythonBase):
    """单例 to python
    default_custom
    not_default_custom
    """
    def setUp(self) -> None:
        super(TestToPythonSingle, self).setUp()

    def test_not_default_init(self):
        """单例 没有默认值 不进行初始化"""
        custom = self.not_default_custom()
        data = to_python(custom)
        self.assertEqual(data, {'name': '_default_params_', 'age': '_default_params_', 'sex': '_default_params_'})

    def test_default_init(self):
        """
        单例 有默认值 不进行初始化
        :return:
        """
        custom = self.default_custom()
        data = to_python(custom)
        self.assertEqual(data, {'age': 10, 'name': 'gaga', 'sex': 1})

    def test_not_default_is_init(self):
        """single, not default, init is True"""
        custom = self.not_default_custom()
        data = to_python(custom, is_init=True)
        self.assertEqual(data, {'name': '_default_params_', 'age': '_default_params_', 'sex': '_default_params_'})

    def test_default_is_init(self):
        """single, default, init is True"""
        custom = self.default_custom()
        data = to_python(custom, is_init=True)
        self.assertEqual(data, {'name': '_default_params_', 'age': '_default_params_', 'sex': '_default_params_'})
