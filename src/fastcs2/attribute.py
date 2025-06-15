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

        self.set_callbacks: list[Callable[[Self], Coroutine[None, None, None]]] = []
        """Callbacks to be called when the attribute is set from an API call"""
        self.update_callbacks: list[Callable[[Self], Coroutine[None, None, None]]] = []
        """Callbacks to be called when the attribute is updated from hardware"""

    def get(self) -> DataTypeT:
        return self._value

    def _set(self, value: Any):
        self._value = self.datatype(value)

    async def set(self, value: Any):
        self._set(value)
        for callback in self.set_callbacks:
            await callback(self)

    async def update(self, value: Any):
        self._set(value)
        for callback in self.update_callbacks:
            await callback(self)

    def __repr__(self):
        return f"{self.name}: {self._value}"
