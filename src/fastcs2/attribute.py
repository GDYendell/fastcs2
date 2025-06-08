from typing import Any, Generic

from fastcs2.attribute_ref import AttrRefT
from fastcs2.datatypes import DataTypeT


class Attribute(Generic[AttrRefT, DataTypeT]):
    def __init__(self, name: str, datatype: type[DataTypeT], ref: AttrRefT):
        self.name = name
        self.datatype = datatype
        self.ref = ref
        self._value = datatype()

    def get(self) -> DataTypeT:
        return self._value

    def set(self, value: Any):
        self._value = self.datatype(value)

    # def send(self, value: str):
    #     pass
