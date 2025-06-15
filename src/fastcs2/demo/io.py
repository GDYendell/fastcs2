from dataclasses import dataclass, field

from psutil import sensors_battery, sensors_temperatures  # type: ignore
from screen_brightness_control import get_brightness, set_brightness  # type: ignore

from fastcs2.attribute import AttributeR
from fastcs2.attribute_ref import AttributeRef
from fastcs2.controller_io import ControllerIO
from fastcs2.datatypes import DataType


class ScreenBrightnessAttrRef(AttributeRef):
    pass


class ScreenBrightnessControllerIO(
    ControllerIO[ScreenBrightnessAttrRef, DataType, DataType]
):
    async def update(self, attr: AttributeR[AttributeRef, DataType]):
        await attr.update(get_brightness()[0])

    async def send(self, value: DataType):
        set_brightness(value)


@dataclass
class SensorsTemperaturesAttrRef(AttributeRef):
    key: str
    index: int
    field: str


class SensorsTemperaturesControllerIO(
    ControllerIO[SensorsTemperaturesAttrRef, DataType, DataType]
):
    def _get_temp(self, ref: SensorsTemperaturesAttrRef) -> int | float | str:
        return getattr(sensors_temperatures()[ref.key][ref.index], ref.field)

    async def update(self, attr: AttributeR[SensorsTemperaturesAttrRef, DataType]):
        await attr.update(self._get_temp(attr.ref))


@dataclass
class SensorsBatteryAttrRef(AttributeRef):
    field: str


class SensorsBatteryControllerIO(
    ControllerIO[SensorsBatteryAttrRef, DataType, DataType]
):
    def _get_battery(self, ref: SensorsBatteryAttrRef) -> int | float | str:
        return getattr(sensors_battery(), ref.field)  # type: ignore

    async def update(self, attr: AttributeR[SensorsBatteryAttrRef, DataType]):
        await attr.update(self._get_battery(attr.ref))


@dataclass
class AverageSummaryAttrRef(AttributeRef):
    attributes: list[AttributeR[AttributeRef, float]] = field(
        default_factory=list[AttributeR[AttributeRef, float]]
    )


class AverageSummaryControllerIO(ControllerIO[AverageSummaryAttrRef, float, DataType]):
    async def update(self, attr: AttributeR[AverageSummaryAttrRef, float]):
        await attr.update(
            sum(attr.get() for attr in attr.ref.attributes) / len(attr.ref.attributes)
        )
