from fastcs2.attribute import Attribute
from fastcs2.attribute_ref import AttributeRef
from fastcs2.controller_io import ControllerIO
from fastcs2.datatypes import DataType


class Controller:
    def __init__(
        self, io: dict[type[AttributeRef], ControllerIO[AttributeRef, DataType]]
    ):
        self.io = io
        self.attributes: list[Attribute[AttributeRef, DataType]] = []

    async def initialise(self):
        pass
