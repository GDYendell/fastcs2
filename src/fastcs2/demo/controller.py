from functools import cached_property

from fastcs2.attribute import Attribute, AttributeR, AttributeRW
from fastcs2.attribute_ref import AttributeRef
from fastcs2.controller import Controller
from fastcs2.controller_io import ControllerIO
from fastcs2.datatypes import DataType
from fastcs2.demo.io import (
    AverageSummaryAttrRef,
    AverageSummaryControllerIO,
    ScreenBrightnessAttrRef,
    ScreenBrightnessControllerIO,
    SensorsBatteryAttrRef,
    SensorsBatteryControllerIO,
    SensorsTemperaturesAttrRef,
    SensorsTemperaturesControllerIO,
)

IO_MAP: dict[type[AttributeRef], ControllerIO[AttributeRef, DataType]] = {
    ScreenBrightnessAttrRef: ScreenBrightnessControllerIO(),
    SensorsBatteryAttrRef: SensorsBatteryControllerIO(),
    SensorsTemperaturesAttrRef: SensorsTemperaturesControllerIO(),
    AverageSummaryAttrRef: AverageSummaryControllerIO(),
}


class SystemMonitorController(Controller):
    cpu_temp = AttributeR(
        "cpu_temp",
        float,
        SensorsTemperaturesAttrRef("k10temp", 0, "current"),
    )
    gpu_temp = AttributeR(
        "gpu_temp",
        float,
        SensorsTemperaturesAttrRef("amdgpu", 0, "current"),
    )
    battery_level = AttributeR(
        "battery_level",
        float,
        SensorsBatteryAttrRef("percent"),
    )
    screen_brightness = AttributeRW(
        "screen_brightness",
        float,
        ScreenBrightnessAttrRef(),
    )

    @cached_property
    def _temperature_attributes(self) -> list[AttributeR[AttributeRef, float]]:
        temperature_attributes: list[AttributeR[AttributeRef, float]] = []
        for attribute in self.attributes:
            if attribute.name.startswith("temp_"):
                assert issubclass(attribute.datatype, float)
                temperature_attributes.append(attribute)  # type:ignore

        return temperature_attributes

    # TODO
    # @attr
    # @property
    # def temp_average(self) -> float:
    #     return sum(attr.get() for attr in self._temperature_attributes) / len(
    #         self._temperature_attributes
    #     )

    def __init__(self):
        self.temp_average = AttributeR(
            "temp_average",
            float,
            AverageSummaryAttrRef([self.cpu_temp, self.gpu_temp]),
        )

        super().__init__(IO_MAP)
