from dataclasses import dataclass, field
from typing import Generic

from fastcs2.attribute import Attribute
from fastcs2.attribute_ref import AttrRefT
from fastcs2.controller_io import ControllerIO
from fastcs2.datatypes import DataType


@dataclass
class Controller(Generic[AttrRefT]):
    io: ControllerIO[AttrRefT]
    attributes: list[Attribute[AttrRefT, DataType]] = field(
        default_factory=list[Attribute[AttrRefT, DataType]]
    )
