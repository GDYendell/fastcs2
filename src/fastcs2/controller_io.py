from typing import Generic

from fastcs2.attribute import Attribute, DataTypeT
from fastcs2.attribute_ref import AttrRefT


class ControllerIO(Generic[AttrRefT, DataTypeT]):
    async def update(self, attr: Attribute[AttrRefT, DataTypeT]):
        pass

    async def send(self, attr: Attribute[AttrRefT, DataTypeT]):
        pass
