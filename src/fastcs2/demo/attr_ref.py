from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from fastcs2.attribute_ref import AttributeRef


@dataclass
class SystemMonitorAttrRef(AttributeRef):
    fn: Callable[[], dict[str, Any]]
    key: str
    index: int
    field: str
