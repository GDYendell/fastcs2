from collections import defaultdict
from collections.abc import Callable, Coroutine
from functools import partial

from fastcs2.attribute import Attribute, AttributeR, AttributeRW, AttributeW
from fastcs2.attribute_io import AttributeIO
from fastcs2.attribute_io_ref import AttributeIORef
from fastcs2.controller_api import ControllerAPI
from fastcs2.datatypes import DataType

type AnyAttributeIO = AttributeIO[AttributeIORef, DataType, DataType]

class Controller:
    def __init__(self, attribute_io: AnyAttributeIO | list[AnyAttributeIO]):
        if not isinstance(attribute_io, list):
            attribute_io = [attribute_io]

        self._attribute_ref_io_map = {io.ref: io for io in attribute_io}
        self.attributes: list[Attribute[AttributeIORef, DataType]] = []

        self._bind_attrs()
        self._link_attr_put_send_callbacks()

    def _bind_attrs(self):
        for attribute_name in dir(self):
            if attribute_name.startswith("_"):
                continue

            attribute = getattr(self, attribute_name)
            if isinstance(attribute, AttributeR | AttributeW):
                io_ref_cls = type(attribute.io_ref)  # type: ignore
                assert issubclass(io_ref_cls, AttributeIORef)

                assert io_ref_cls in self._attribute_ref_io_map, (
                    f"{self.__class__.__name__} does not have an AttributeIO to handle "
                    f"{io_ref_cls.__name__}"
                )

                self.attributes.append(attribute)  # type: ignore

    async def initialise(self):
        pass

    def create_update_tasks(
        self,
    ) -> dict[float, list[Callable[[], Coroutine[None, None, None]]]]:
        update_tasks: dict[float, list[Callable[[], Coroutine[None, None, None]]]] = (
            defaultdict(list)
        )
        for attribute in self.attributes:
            if isinstance(attribute, AttributeR) and attribute.io_ref.update_period:
                update_tasks[attribute.io_ref.update_period].append(
                    partial(
                        self._attribute_ref_io_map[type(attribute.io_ref)].update,
                        attribute,
                    )
                )

        return update_tasks

    def _link_attr_put_send_callbacks(self):
        for attribute in self.attributes:
            if isinstance(attribute, AttributeRW):
                attribute.put_callbacks.append(
                    self._attribute_ref_io_map[type(attribute.io_ref)].send
                )

    def build_api(self) -> ControllerAPI:
        return ControllerAPI(self.attributes)
