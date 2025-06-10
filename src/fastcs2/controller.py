from collections.abc import Callable, Coroutine
from functools import partial

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

        self._bind_attrs()

    def _bind_attrs(self):
        for attribute_name in dir(self):
            if attribute_name.startswith("_"):
                continue

            attribute = getattr(self, attribute_name)
            if isinstance(attribute, Attribute):
                io_type = type(attribute.ref)  # type: ignore
                assert issubclass(io_type, AttributeRef)

                self.attributes.append(attribute)  # type: ignore

    async def initialise(self):
        pass

    def create_update_tasks(
        self,
    ) -> list[Callable[[], Coroutine[None, None, None]]]:
        return [
            partial(self.io[type(attribute.ref)].update, attribute)
            for attribute in self.attributes
        ]
