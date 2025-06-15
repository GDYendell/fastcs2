from collections.abc import Callable, Coroutine
from functools import partial

from fastcs2.attribute import Attribute, AttributeR, AttributeRW, AttributeW
from fastcs2.attribute_ref import AttributeRef
from fastcs2.controller_api import ControllerAPI
from fastcs2.controller_io import ControllerIO
from fastcs2.datatypes import DataType


class Controller:
    def __init__(
        self,
        io: dict[type[AttributeRef], ControllerIO[AttributeRef, DataType, DataType]],
    ):
        self.io = io
        self.attributes: list[Attribute[AttributeRef, DataType]] = []

        self._bind_attrs()
        self._link_attr_put_send_callbacks()

    def _bind_attrs(self):
        for attribute_name in dir(self):
            if attribute_name.startswith("_"):
                continue

            attribute = getattr(self, attribute_name)
            if isinstance(attribute, AttributeR | AttributeW):
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
            if isinstance(attribute, AttributeR)
        ]

    def _link_attr_put_send_callbacks(self):
        for attribute in self.attributes:
            if isinstance(attribute, AttributeRW):
                attribute.put_callbacks.append(self.io[type(attribute.ref)].send)

    def build_api(self) -> ControllerAPI:
        return ControllerAPI(self.attributes)
