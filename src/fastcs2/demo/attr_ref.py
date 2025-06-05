from dataclasses import dataclass

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
    pattern: str


SystemMonitorAttributeRef = SensorsTemperaturesAttrRef | SensorsBatteryAttrRef
