from collections.abc import Callable
from functools import partial
from typing import Any

from fastcs2.attribute import AttributeR
from fastcs2.attribute_io_ref import AttributeIORef
from fastcs2.controller_api import ControllerAPI
from fastcs2.datatypes import DataType


class Transport:
    def __init__(self, api: ControllerAPI):
        self.api = api

    @property
    def context(self) -> dict[str, Callable[..., Any]]:
        return {}


async def print_attribute(path: list[str], attr: AttributeR[AttributeIORef, DataType]):
    print(f"{'.'.join(path + [attr.name])}: {attr.get()}")


class ConsoleTransport(Transport):
    def __init__(self, api: ControllerAPI):
        super().__init__(api)

        for controller in api.walk_controllers():
            for attribute in controller.attributes.values():
                if isinstance(attribute, AttributeR):
                    attribute.update_callbacks.append(
                        partial(print_attribute, controller.path)
                    )

    async def print_all(self):
        print("\n---ConsoleTransport Print\n")
        for controller in self.api.walk_controllers():
            for attribute in controller.attributes.values():
                await print_attribute(controller.path, attribute)
        print("\n---ConsoleTransport Print End\n")

    @property
    def context(self):
        return {"print_all": self.print_all}
