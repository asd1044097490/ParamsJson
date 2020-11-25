import unittest

from params_json import Params, CharField, IntField, to_python, to_class, to_instance
from params_json.check import check, check_list
from params_json.params import initialization_cls


class TestCheck(unittest.TestCase):

    def setUp(self) -> None:
        class Custom(Params):
            name = CharField()
            age = IntField(default=18)

        class Family(Params):
            family = Custom(many=True)
            count = IntField(default=1)

        self.custom = Custom
        self.family = Family

    def test_check(self):
        family = self.family()
        # check(self.custom())
        # data = {'family': [{'name': '_default_params_', 'age': 18}], 'count': 1}
        # data = {'family': [{'name': '1'}], 'count': 1}
        # print(data)
        print(to_python(family))
        print(initialization_cls(family))
        print(to_python(family))

        # cls = to_class(data, family)
        # check_list(cls.family)
        # print(to_instance(cls.family)['name'].params_default)
        # print(to_instance(cls.family)['age'].params_default)
