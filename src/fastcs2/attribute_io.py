from typing import Generic

from fastcs2.attribute import AttributeR, DataTypeT
from fastcs2.attribute_io_ref import AttributeIORefT
from fastcs2.datatypes import DataTypeInT


class AttributeIO(Generic[AttributeIORefT, DataTypeT, DataTypeInT]):
    def __init__(self, io_ref: type[AttributeIORefT]):
        self.ref = io_ref

    async def update(self, attr: AttributeR[AttributeIORefT, DataTypeT]):
        pass

    async def send(self, value: DataTypeInT):
        pass
