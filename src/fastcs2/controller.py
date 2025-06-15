from collections.abc import Callable, Coroutine
from functools import partial

from fastcs2.attribute import Attribute, AttributeR, AttributeRW, AttributeW
from fastcs2.attribute_io import AttributeIO
from fastcs2.attribute_io_ref import AttributeIORef
from fastcs2.controller_api import ControllerAPI
from fastcs2.datatypes import DataType


class Controller:
    def __init__(
        self,
        io: dict[type[AttributeIORef], AttributeIO[AttributeIORef, DataType, DataType]],
    ):
        self.io = io
        self.attributes: list[Attribute[AttributeIORef, DataType]] = []

        self._bind_attrs()
        self._link_attr_put_send_callbacks()

    def _bind_attrs(self):
        for attribute_name in dir(self):
            if attribute_name.startswith("_"):
                continue

            attribute = getattr(self, attribute_name)
            if isinstance(attribute, AttributeR | AttributeW):
                io_type = type(attribute.io)  # type: ignore
                assert issubclass(io_type, AttributeIORef)

                self.attributes.append(attribute)  # type: ignore

    async def initialise(self):
        pass

    def create_update_tasks(
        self,
    ) -> list[Callable[[], Coroutine[None, None, None]]]:
        return [
            partial(self.io[type(attribute.io)].update, attribute)
            for attribute in self.attributes
            if isinstance(attribute, AttributeR)
        ]

    def _link_attr_put_send_callbacks(self):
        for attribute in self.attributes:
            if isinstance(attribute, AttributeRW):
                attribute.put_callbacks.append(self.io[type(attribute.io)].send)

    def build_api(self) -> ControllerAPI:
        return ControllerAPI(self.attributes)
