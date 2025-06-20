from functools import cached_property

from fastcs2 import AttributeIORef, AttributeR, AttributeRW, Controller
from fastcs2.demo.attribute_io import (
    AverageSummaryAttributeIO,
    AverageSummaryAttributeIORef,
    ScreenBrightnessAttributeIO,
    ScreenBrightnessAttributeIORef,
    SensorsBatteryAttributeIO,
    SensorsBatteryAttributeIORef,
    SensorsTemperaturesAttributeIO,
    SensorsTemperaturesAttributeIORef,
)


class SystemMonitorController(Controller):
    cpu_temp = AttributeR(
        "cpu_temp",
        float,
        SensorsTemperaturesAttributeIORef("k10temp", 0, "current"),
    )
    gpu_temp = AttributeR(
        "gpu_temp",
        float,
        SensorsTemperaturesAttributeIORef("amdgpu", 0, "current"),
    )
    battery_level = AttributeR(
        "battery_level",
        float,
        SensorsBatteryAttributeIORef("percent"),
    )
    screen_brightness = AttributeRW(
        "screen_brightness",
        float,
        ScreenBrightnessAttributeIORef(),
    )

    @cached_property
    def _temperature_attributes(self) -> list[AttributeR[AttributeIORef, float]]:
        temperature_attributes: list[AttributeR[AttributeIORef, float]] = []
        for attribute in self._attributes.values():
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
            AverageSummaryAttributeIORef([self.cpu_temp, self.gpu_temp]),
        )

        super().__init__(
            [
                AverageSummaryAttributeIO(),
                ScreenBrightnessAttributeIO(),
                SensorsBatteryAttributeIO(),
                SensorsTemperaturesAttributeIO(),
            ]
        )
