from typing import Dict, Union

from pydantic import BaseModel

from polyfactory.factories.pydantic_factory import ModelFactory


def test_passing_nested_dict() -> None:
    class MyMappedClass(BaseModel):
        val: str

    class MyClass(BaseModel):
        my_mapping_obj: Dict[str, MyMappedClass]
        my_mapping_str: Dict[str, str]

    class MyClassFactory(ModelFactory[MyClass]):
        __model__ = MyClass

    obj = MyClassFactory.build(
        my_mapping_str={"foo": "bar"},
        my_mapping_obj={"baz": MyMappedClass(val="bar")},
    )

    assert obj.dict() == {"my_mapping_obj": {"baz": {"val": "bar"}}, "my_mapping_str": {"foo": "bar"}}


def test_dict_with_union_random_types() -> None:
    class MyClass(BaseModel):
        val: Dict[str, Union[int, str]]

    class MyClassFactory(ModelFactory[MyClass]):
        __model__ = MyClass

    MyClassFactory.seed_random(2)

    test_obj_1 = MyClassFactory.build()
    test_obj_2 = MyClassFactory.build()

    assert isinstance(list(test_obj_1.val.values())[0], int)
    assert isinstance(list(test_obj_2.val.values())[0], str)
