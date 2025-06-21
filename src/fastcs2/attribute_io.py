from typing import Generic

from fastcs2.attribute import AttributeR, AttributeRW, DataTypeT
from fastcs2.attribute_io_ref import AttributeIORef, AttributeIORefT
from fastcs2.datatypes import DataType, DataTypeInT


class AttributeIO(Generic[AttributeIORefT, DataTypeT, DataTypeInT]):
    def __init__(self, io_ref: type[AttributeIORefT]):
        self.ref = io_ref

    async def update(self, attr: AttributeR[AttributeIORefT, DataTypeT]) -> None:
        raise NotImplementedError()

    async def send(
        self, attr: AttributeRW[AttributeIORefT, DataTypeT], value: DataTypeInT
    ) -> None:
        raise NotImplementedError()


AnyAttributeIO = AttributeIO[AttributeIORef, DataType, DataType]
