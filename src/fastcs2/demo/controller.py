from psutil import sensors_temperatures

from fastcs2.attribute import Attribute
from fastcs2.controller import Controller
from fastcs2.demo.attr_ref import SystemMonitorAttrRef


class SystemMonitorController(Controller[SystemMonitorAttrRef]):
    cpu_temp = Attribute(
        "state",
        float,
        SystemMonitorAttrRef(sensors_temperatures, "k10temp", 0, "current"),
    )

    # @attr
    # def gpu_temp(self) -> float:
    #     return sensors_temperatures()["k10temp"][1].current
