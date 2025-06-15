from collections.abc import Callable, Coroutine
from typing import Any, Generic, Self

from fastcs2.attribute_ref import AttrRefT
from fastcs2.datatypes import DataTypeT


class Attribute(Generic[AttrRefT, DataTypeT]):
    def __init__(self, name: str, datatype: type[DataTypeT], ref: AttrRefT):
        self.name = name
        self.datatype = datatype
        self.ref = ref

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name},  {self.datatype.__name__})"


class AttributeR(Attribute[AttrRefT, DataTypeT]):
    def __init__(self, name: str, datatype: type[DataTypeT], ref: AttrRefT):
        super().__init__(name, datatype, ref)

        self._value = datatype()

        self.update_callbacks: list[Callable[[Self], Coroutine[None, None, None]]] = []
        """Callbacks to be called when the attribute is updated from hardware"""

    def get(self) -> DataTypeT:
        return self._value

    def _set(self, value: Any):
        self._value = self.datatype(value)

    async def update(self, value: Any):
        self._set(value)
        for callback in self.update_callbacks:
            await callback(self)


class AttributeW(Attribute[AttrRefT, DataTypeT]):
    def __init__(self, name: str, datatype: type[DataTypeT], ref: AttrRefT):
        super().__init__(name, datatype, ref)

        self.put_callbacks: list[
            Callable[[DataTypeT], Coroutine[None, None, None]]
        ] = []
        """Callbacks to be called when the attribute is set from an API call"""

    async def put(self, value: Any):
        for callback in self.put_callbacks:
            await callback(value)


class AttributeRW(AttributeR[AttrRefT, DataTypeT], AttributeW[AttrRefT, DataTypeT]):
    def __init__(self, name: str, datatype: type[DataTypeT], ref: AttrRefT):
        super().__init__(name, datatype, ref)

    async def put(self, value: Any):
        await super().put(value)
        self._set(value)
