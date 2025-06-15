from fastcs2.attribute import AttributeR
from fastcs2.attribute_ref import AttributeRef
from fastcs2.controller_api import ControllerAPI
from fastcs2.datatypes import DataType


class Transport:
    def __init__(self, api: ControllerAPI):
        self.api = api


async def print_attr_update(attr: AttributeR[AttributeRef, DataType]):
    print(f"{attr.name}: {attr.get()}")


class ConsoleTransport(Transport):
    def __init__(self, api: ControllerAPI):
        super().__init__(api)

        for attribute in api.attributes:
            if isinstance(attribute, AttributeR):
                attribute.update_callbacks.append(print_attr_update)
