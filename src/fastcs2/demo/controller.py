from fastcs2.attribute import Attribute
from fastcs2.controller import Controller
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

    # @attr
    # def gpu_temp(self) -> float:
    #     return sensors_temperatures()["k10temp"][1].current

    def __init__(self):
        super().__init__(
            {
                SensorsBatteryAttrRef: SensorsBatteryControllerIO(),
                SensorsTemperaturesAttrRef: SensorsTemperaturesControllerIO(),
                AverageSummaryAttrRef: AverageSummaryControllerIO(),
            }
        )
        self.temp_average = Attribute(
            "temp_average",
            float,
            AverageSummaryAttrRef([self.cpu_temp, self.gpu_temp]),
        )
