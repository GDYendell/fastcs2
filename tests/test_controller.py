import pytest

from fastcs2.attribute import AttributeR
from fastcs2.attribute_io import AttributeIO
from fastcs2.attribute_io_ref import AttributeIORef
from fastcs2.controller import Controller
from fastcs2.datatypes import DataType
from fastcs2.demo.attribute_io import SensorsTemperaturesAttributeIORef
from fastcs2.demo.controller import SystemMonitorController


class MyAttributeIORef(AttributeIORef):
    pass


class MyAttributeIO(AttributeIO[MyAttributeIORef, DataType, DataType]):
    def __init__(self):
        super().__init__(MyAttributeIORef)

    async def update(self, attr: AttributeR[MyAttributeIORef, DataType]):
        await attr.update("ON")


class MyController(Controller):
    def __init__(self):
        super().__init__(MyAttributeIO())
        self.state = AttributeR("state", str, MyAttributeIORef())


@pytest.mark.asyncio
async def test_controller():
    controller = MyController()

    assert controller.state.get() == ""
    await controller._attribute_ref_io_map[MyAttributeIORef].update(controller.state)  # type: ignore
    assert controller.state.get() == "ON"


@pytest.mark.asyncio
async def test_sys_controller():
    controller = SystemMonitorController()

    assert controller.cpu_temp.get() == 0.0
    await controller._attribute_ref_io_map[SensorsTemperaturesAttributeIORef].update(  # type: ignore
        controller.cpu_temp
    )
    assert isinstance(controller.cpu_temp.get(), float)
