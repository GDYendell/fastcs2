import pytest

from fastcs2.attribute import AttributeR
from fastcs2.attribute_ref import AttributeRef
from fastcs2.controller import Controller
from fastcs2.controller_io import ControllerIO
from fastcs2.datatypes import DataType
from fastcs2.demo.controller import SystemMonitorController
from fastcs2.demo.io import SensorsTemperaturesAttrRef


class MyAttrRef(AttributeRef):
    pass


class MyControllerIO(ControllerIO[MyAttrRef, DataType, DataType]):
    async def update(self, attr: AttributeR[MyAttrRef, DataType]):
        await attr.update(attr.datatype("ON"))


class MyController(Controller):
    def __init__(self, io: MyControllerIO):
        super().__init__({MyAttrRef: io})
        self.state = AttributeR("state", str, MyAttrRef())


@pytest.mark.asyncio
async def test_controller():
    controller = MyController(MyControllerIO())

    assert controller.state.get() == ""
    await controller.io[MyAttrRef].update(controller.state)
    assert controller.state.get() == "ON"


@pytest.mark.asyncio
async def test_sys_controller():
    controller = SystemMonitorController()

    assert controller.cpu_temp.get() == 0.0
    await controller.io[SensorsTemperaturesAttrRef].update(controller.cpu_temp)
    assert isinstance(controller.cpu_temp.get(), float)
