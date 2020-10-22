# ParamsJson
params class to dict    
dict to class

    1.通过python的class定义整个data的数据结构
    2.

### class to python (dict)
#### to_python
##### 单例
```python
from params_json import to_python, Field, Params

class Custom(Params):
    name = Field(default='gaga')
    age = Field(default=16)


result = to_python(Custom())    
result: {"name": "gaga", "age": 16}
```
##### 嵌套 dict
```python
from params_json import to_python, Field, Params

class Custom(Params):
    name = Field(default='gaga')
    age = Field(default=18)


class Family(Params):
    family = Custom()
    count = Field(default=1)


result = to_python(Family())
result: {'family': {'name': 'gaga', 'age': 18}, 'count': 1}
```
##### 嵌套 list
```python
from params_json import to_python, Field, Params

class Custom(Params):
    name = Field(default='gaga')
    age = Field(default=18)


class Family(Params):
    family = Custom(many=True, many_number=1)
    count = Field(default=1)


result = to_python(Family())
result: {'family': [{'name': 'gaga', 'age': 18}], 'count': 1}
```
#### to_class
```python
from params_json import to_class, to_python, Field, Params
class Custom(Params):
    name = Field(default='gaga')
    age = Field(default=16)


result = to_python(Custom())    
result: {"name": "gaga", "age": 16}
cls = to_class(result, Custom())

```