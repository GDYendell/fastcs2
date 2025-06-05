import pytest

from fastcs2.attribute import Attribute, DataTypeT
from fastcs2.attribute_ref import AttributeRef
from fastcs2.controller import Controller
from fastcs2.controller_io import ControllerIO
from fastcs2.demo.controller import SystemMonitorController
from fastcs2.demo.controller_io import SensorsTemperaturesControllerIO


class MyAttrRef(AttributeRef):
    pass


class MyControllerIO(ControllerIO[MyAttrRef]):
    async def update(self, attr: Attribute[DataTypeT, MyAttrRef]):
        attr.set(attr.datatype("ON"))


class MyController(Controller[MyAttrRef]):
    state = Attribute("state", str, MyAttrRef())


@pytest.mark.asyncio
async def test_controller():
    controller = MyController(MyControllerIO())

    assert controller.state.get() == ""
    await controller.io.update(controller.state)
    assert controller.state.get() == "ON"


@pytest.mark.asyncio
async def test_sys_controller():
    controller = SystemMonitorController(SensorsTemperaturesControllerIO())

    assert controller.cpu_temp.get() == 0.0
    await controller.io.update(controller.cpu_temp)
    print(controller.cpu_temp.get())
    assert isinstance(controller.cpu_temp.get(), float)
