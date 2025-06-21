from functools import partial

from fastcs2.attribute import AttributeR
from fastcs2.attribute_io_ref import AttributeIORef
from fastcs2.controller_api import ControllerAPI
from fastcs2.datatypes import DataType


class Transport:
    def __init__(self, api: ControllerAPI):
        self.api = api


async def print_attr_update(
    path: list[str], attr: AttributeR[AttributeIORef, DataType]
):
    print(f"{'.'.join(path + [attr.name])}: {attr.get()}")


class ConsoleTransport(Transport):
    def __init__(self, api: ControllerAPI):
        super().__init__(api)

        for controller in api.walk_controllers():
            for attribute in controller.attributes.values():
                if isinstance(attribute, AttributeR):
                    attribute.update_callbacks.append(
                        partial(print_attr_update, controller.path)
                    )
