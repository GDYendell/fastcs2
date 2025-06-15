from dataclasses import dataclass

from fastcs2.attribute import Attribute
from fastcs2.attribute_io_ref import AttributeIORef
from fastcs2.datatypes import DataType


@dataclass(frozen=True)
class ControllerAPI:
    attributes: list[Attribute[AttributeIORef, DataType]]
