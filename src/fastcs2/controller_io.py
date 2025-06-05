from collections.abc import Sequence
from typing import Generic

from fastcs2.attribute import Attribute, DataTypeT
from fastcs2.attribute_ref import AttrRefT
from fastcs2.datatypes import DataType


class ControllerIO(Generic[AttrRefT, DataTypeT]):
    async def initialise(
        self,
        attr: Attribute[AttrRefT, DataTypeT],
        all_attributes: Sequence[Attribute[AttrRefT, DataType]],
    ):
        pass

    async def update(self, attr: Attribute[AttrRefT, DataTypeT]):
        pass

    async def send(self, attr: Attribute[AttrRefT, DataTypeT]):
        pass
