from typing import Generic

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

    def set(self, value: DataTypeT):
        self._value = value

    # def send(self, value: str):
    #     pass
