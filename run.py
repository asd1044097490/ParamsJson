
from serializers.fields import Object, Field


class Custom(Object):
    name = Field()
    age = Field()


class Family(Object):
    family = Custom()
    count = Field()


if __name__ == "__main__":
    # data = {'name': 'jiajintao', 'age': 19}
    # custom = Custom(data=data)
    # custom.init_data()
    
    # custom.check()
    # print(custom._errors)
    data = {'count': 2, 'family': {'name': 'jia', 'age': 18}}
    family = Family(data=data)
    family.init_data()
    family
    # print(getattr(family, 'count', None)().data)
    # print(family.count.data)
    # print(family._errors)
