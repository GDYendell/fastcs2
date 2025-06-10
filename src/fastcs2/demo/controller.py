from functools import cached_property

from fastcs2.attribute import Attribute
from fastcs2.attribute_ref import AttributeRef
from fastcs2.controller import Controller
from fastcs2.controller_io import ControllerIO
from fastcs2.datatypes import DataType
from fastcs2.demo.attr_ref import (
    AverageSummaryAttrRef,
    SensorsBatteryAttrRef,
    SensorsTemperaturesAttrRef,
)
from fastcs2.demo.controller_io import (
    AverageSummaryControllerIO,
    SensorsBatteryControllerIO,
    SensorsTemperaturesControllerIO,
)

IO_MAP: dict[type[AttributeRef], ControllerIO[AttributeRef, DataType]] = {
    SensorsBatteryAttrRef: SensorsBatteryControllerIO(),
    SensorsTemperaturesAttrRef: SensorsTemperaturesControllerIO(),
    AverageSummaryAttrRef: AverageSummaryControllerIO(),
}


class SystemMonitorController(Controller):
    cpu_temp = Attribute(
        "cpu_temp",
        float,
        SensorsTemperaturesAttrRef("k10temp", 0, "current"),
    )
    gpu_temp = Attribute(
        "gpu_temp",
        float,
        SensorsTemperaturesAttrRef("amdgpu", 0, "current"),
    )
    battery_level = Attribute(
        "battery_level",
        float,
        SensorsBatteryAttrRef("percent"),
    )

    @cached_property
    def _temperature_attributes(self) -> list[Attribute[AttributeRef, float]]:
        temperature_attributes: list[Attribute[AttributeRef, float]] = []
        for attribute in self.attributes:
            if attribute.name.startswith("temp_"):
                assert issubclass(attribute.datatype, float)
                temperature_attributes.append(attribute)  # type:ignore

        return temperature_attributes

    # TODO
    # @attr
    # def temp_average(self) -> float:
    #     return sum(attr.get() for attr in self._temperature_attributes) / len(
    #         self._temperature_attributes
    #     )

    def __init__(self):
        self.temp_average = Attribute(
            "temp_average",
            float,
            AverageSummaryAttrRef([self.cpu_temp, self.gpu_temp]),
        )

        super().__init__(IO_MAP)
