import unittest

from params_json import Params, CharField, IntField, to_python, to_class


class Base(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        class Custom(Params):
            name = CharField(default='gaga')
            age = IntField(default=18)

        cls.custom = Custom


class TestToPythonSingle(Base):

    def test_to_python(self):
        custom = self.custom()
        data = to_python(custom)
        self.assertEqual(data, {'name': 'gaga', 'age': 18})

    def test_to_python_update(self):
        custom = self.custom(content={'name': 'gaga1'})
        self.assertEqual(to_python(custom, is_default=True), {'name': 'gaga1', 'age': 18})


class TestToClassSingle(Base):

    def test_to_class(self):
        custom = self.custom()
        data = to_python(custom)
        cls = to_class(data, custom)
        self.assertIsInstance(cls, self.custom)

    def test_to_class_update(self):
        data = {
            'name': 'gaga2', 'age': 100
        }
        cls = to_class(data, self.custom())
        self.assertIsInstance(cls, self.custom)
        _data = to_python(cls)
        self.assertEqual(data, _data)


class TestNestDict(unittest.TestCase):

    def setUp(self) -> None:
        class Custom(Params):
            name = CharField(default='gaga')
            age = IntField(default=29)

        class Family(Params):
            family = Custom()
            count = IntField(default=5)

        self.family = Family
        self.Custom = Custom

    def test_to_python(self):
        data = to_python(self.family())
        self.assertEqual(data, {'family': {'name': 'gaga', 'age': 29}, 'count': 5})

    def test_to_class(self):
        data = {'family': {'name': 'gaga', 'age': 29}, 'count': 5}
        cls = to_class(data, self.family())
        self.assertIsInstance(cls, self.family)
        self.assertEqual(to_python(cls), data)