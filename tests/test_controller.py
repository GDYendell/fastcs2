import pytest

from fastcs2.attribute import AttributeR
from fastcs2.attribute_io import AttributeIO, AttributeIORef
from fastcs2.controller import Controller
from fastcs2.datatypes import DataType
from fastcs2.demo.attribute_io import SensorsTemperaturesAttributeIORef
from fastcs2.demo.controller import SystemMonitorController


class MyAttributeIO(AttributeIORef):
    pass


class MyAttributeIO(AttributeIO[MyAttributeIO, DataType, DataType]):
    async def update(self, attr: AttributeR[MyAttributeIO, DataType]):
        await attr.update(attr.datatype("ON"))


class MyController(Controller):
    def __init__(self, io: MyAttributeIO):
        super().__init__({MyAttributeIO: io})
        self.state = AttributeR("state", str, MyAttributeIO())


@pytest.mark.asyncio
async def test_controller():
    controller = MyController(MyAttributeIO())

    assert controller.state.get() == ""
    await controller.io[MyAttributeIO].update(controller.state)
    assert controller.state.get() == "ON"


@pytest.mark.asyncio
async def test_sys_controller():
    controller = SystemMonitorController()

    assert controller.cpu_temp.get() == 0.0
    await controller.io[SensorsTemperaturesAttributeIORef].update(controller.cpu_temp)
    assert isinstance(controller.cpu_temp.get(), float)
