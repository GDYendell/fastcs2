from fastcs2.attribute import Attribute
from fastcs2.attribute_ref import AttributeRef
from fastcs2.controller_api import ControllerAPI
from fastcs2.datatypes import DataType


class Transport:
    def __init__(self, api: ControllerAPI):
        self.api = api


async def log_attr_update(attr: Attribute[AttributeRef, DataType]):
    print(f"{attr.name}: {attr.get()}")


class LogTransport(Transport):
    def __init__(self, api: ControllerAPI):
        super().__init__(api)

        for attribute in api.attributes:
            attribute.update_callbacks.append(log_attr_update)
