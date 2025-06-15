from collections.abc import Callable, Coroutine
from typing import Any, Generic, Self

from fastcs2.attribute_ref import AttrRefT
from fastcs2.datatypes import DataTypeT


class Attribute(Generic[AttrRefT, DataTypeT]):
    def __init__(self, name: str, datatype: type[DataTypeT], ref: AttrRefT):
        self.name = name
        self.datatype = datatype
        self.ref = ref
        self._value = datatype()
        self.send_callbacks: list[Callable[[Self], Coroutine[None, None, None]]] = []

    def get(self) -> DataTypeT:
        return self._value

    def set(self, value: Any):
        self._value = self.datatype(value)

    async def put(self, value: Any):
        self.set(value)
        for callback in self.send_callbacks:
            await callback(self)

    def __repr__(self):
        return f"{self.name}: {self._value}"
