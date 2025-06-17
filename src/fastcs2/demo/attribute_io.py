from dataclasses import dataclass, field

from psutil import sensors_battery, sensors_temperatures  # type: ignore
from screen_brightness_control import get_brightness, set_brightness  # type: ignore

from fastcs2.attribute import AttributeR
from fastcs2.attribute_io import AttributeIO
from fastcs2.attribute_io_ref import AttributeIORef
from fastcs2.datatypes import DataType


class ScreenBrightnessAttributeIORef(AttributeIORef):
    pass


class ScreenBrightnessAttributeIO(
    AttributeIO[ScreenBrightnessAttributeIORef, DataType, DataType]
):
    def __init__(self):
        super().__init__(ScreenBrightnessAttributeIORef)

    async def update(self, attr: AttributeR[AttributeIORef, DataType]):
        await attr.update(get_brightness()[0])

    async def send(self, value: DataType):
        set_brightness(value)


@dataclass
class SensorsTemperaturesAttributeIORef(AttributeIORef):
    key: str
    index: int
    field: str


class SensorsTemperaturesAttributeIO(
    AttributeIO[SensorsTemperaturesAttributeIORef, DataType, DataType]
):
    def __init__(self):
        super().__init__(SensorsTemperaturesAttributeIORef)

    async def update(
        self, attr: AttributeR[SensorsTemperaturesAttributeIORef, DataType]
    ):
        await attr.update(
            getattr(
                sensors_temperatures()[attr.io_ref.key][attr.io_ref.index],
                attr.io_ref.field,
            )
        )


@dataclass
class SensorsBatteryAttributeIORef(AttributeIORef):
    field: str


class SensorsBatteryAttributeIO(
    AttributeIO[SensorsBatteryAttributeIORef, DataType, DataType]
):
    def __init__(self):
        super().__init__(SensorsBatteryAttributeIORef)

    async def update(self, attr: AttributeR[SensorsBatteryAttributeIORef, DataType]):
        await attr.update(getattr(sensors_battery(), attr.io_ref.field))  # type: ignore


@dataclass
class AverageSummaryAttributeIORef(AttributeIORef):
    attributes: list[AttributeR[AttributeIORef, float]] = field(
        default_factory=list[AttributeR[AttributeIORef, float]]
    )


class AverageSummaryAttributeIO(
    AttributeIO[AverageSummaryAttributeIORef, float, DataType]
):
    def __init__(self):
        super().__init__(AverageSummaryAttributeIORef)

    async def update(self, attr: AttributeR[AverageSummaryAttributeIORef, float]):
        await attr.update(
            sum(attr.get() for attr in attr.io_ref.attributes)
            / len(attr.io_ref.attributes)
        )
