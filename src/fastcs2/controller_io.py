from typing import Generic

from fastcs2.attribute import AttributeR, DataTypeT
from fastcs2.attribute_ref import AttrRefT
from fastcs2.datatypes import DataTypeInT


class ControllerIO(Generic[AttrRefT, DataTypeT, DataTypeInT]):
    async def update(self, attr: AttributeR[AttrRefT, DataTypeT]):
        pass

    async def send(self, value: DataTypeInT):
        pass
