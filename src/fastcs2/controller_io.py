from typing import Generic

from fastcs2.attribute import AttributeR, AttributeRW, DataTypeT
from fastcs2.attribute_ref import AttrRefT


class ControllerIO(Generic[AttrRefT, DataTypeT]):
    async def update(self, attr: AttributeR[AttrRefT, DataTypeT]):
        pass

    async def send(self, attr: AttributeRW[AttrRefT, DataTypeT]):
        pass
