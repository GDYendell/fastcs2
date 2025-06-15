import logging

from psutil import sensors_battery, sensors_temperatures  # type: ignore

from fastcs2.attribute import Attribute
from fastcs2.controller_io import ControllerIO
from fastcs2.datatypes import DataType
from fastcs2.demo.attr_ref import (
    AverageSummaryAttrRef,
    SensorsBatteryAttrRef,
    SensorsTemperaturesAttrRef,
)


class SensorsTemperaturesControllerIO(
    ControllerIO[SensorsTemperaturesAttrRef, DataType]
):
    def _get_temp(self, ref: SensorsTemperaturesAttrRef) -> int | float | str:
        return getattr(sensors_temperatures()[ref.key][ref.index], ref.field)

    async def update(self, attr: Attribute[SensorsTemperaturesAttrRef, DataType]):
        attr.set(self._get_temp(attr.ref))
        logging.info(f"{attr.name}: {attr.get()}")


class SensorsBatteryControllerIO(ControllerIO[SensorsBatteryAttrRef, DataType]):
    def _get_battery(self, ref: SensorsBatteryAttrRef) -> int | float | str:
        return getattr(sensors_battery(), ref.field)  # type: ignore

    async def update(self, attr: Attribute[SensorsBatteryAttrRef, DataType]):
        attr.set(self._get_battery(attr.ref))
        logging.info(f"{attr.name}: {attr.get()}")


class AverageSummaryControllerIO(ControllerIO[AverageSummaryAttrRef, float]):
    async def update(self, attr: Attribute[AverageSummaryAttrRef, float]):
        attr.set(
            sum(attr.get() for attr in attr.ref.attributes) / len(attr.ref.attributes)
        )
        logging.info(f"{attr.name}: {attr.get()}")
