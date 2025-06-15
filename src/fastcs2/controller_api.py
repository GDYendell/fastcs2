from dataclasses import dataclass

from fastcs2.attribute import Attribute
from fastcs2.attribute_ref import AttributeRef
from fastcs2.datatypes import DataType


@dataclass(frozen=True)
class ControllerAPI:
    attributes: list[Attribute[AttributeRef, DataType]]
