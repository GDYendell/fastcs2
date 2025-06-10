from dataclasses import dataclass, field

from fastcs2.attribute import Attribute
from fastcs2.attribute_ref import AttributeRef


@dataclass
class SensorsTemperaturesAttrRef(AttributeRef):
    key: str
    index: int
    field: str


@dataclass
class SensorsBatteryAttrRef(AttributeRef):
    field: str


@dataclass
class AverageSummaryAttrRef(AttributeRef):
    attributes: list[Attribute[AttributeRef, float]] = field(
        default_factory=list[Attribute[AttributeRef, float]]
    )


SystemMonitorAttributeRef = SensorsTemperaturesAttrRef | SensorsBatteryAttrRef
