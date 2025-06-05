from collections.abc import Sequence

from psutil import sensors_battery, sensors_temperatures  # type: ignore

from fastcs2.attribute import Attribute
from fastcs2.attribute_ref import AttributeRef
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
        attr.set(attr.datatype(self._get_temp(attr.ref)))
        print(f"{attr.name}: {attr.get()}")


class SensorsBatteryControllerIO(ControllerIO[SensorsBatteryAttrRef, DataType]):
    def _get_battery(self, ref: SensorsBatteryAttrRef) -> int | float | str:
        return getattr(sensors_battery(), ref.field)  # type: ignore

    async def update(self, attr: Attribute[SensorsBatteryAttrRef, DataType]):
        attr.set(attr.datatype(self._get_battery(attr.ref)))
        print(f"{attr.name}: {attr.get()}")


class AverageSummaryControllerIO(ControllerIO[AverageSummaryAttrRef, float]):
    attributes: list[Attribute[AverageSummaryAttrRef, float]] = []

    async def initialise(
        self,
        attr: Attribute[AverageSummaryAttrRef, float],
        all_attributes: Sequence[Attribute[AttributeRef, DataType]],
    ):
        for other_attr in all_attributes:
            if attr is other_attr:
                continue
            elif not isinstance(other_attr.datatype, type(float)):
                continue

            if attr.ref.pattern in other_attr.name:
                self.attributes.append(other_attr)

    async def update(self, attr: Attribute[AverageSummaryAttrRef, float]):
        attr.set(
            attr.datatype(
                sum(attr.get() for attr in self.attributes) / len(self.attributes)
            )
        )
        print(f"{attr.name}: {attr.get()}")
