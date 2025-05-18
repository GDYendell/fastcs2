from fastcs2.attribute import Attribute, DataTypeT
from fastcs2.controller_io import ControllerIO
from fastcs2.demo.attr_ref import SystemMonitorAttrRef


class SystemMonitorControllerIO(ControllerIO[SystemMonitorAttrRef]):
    def _get_sensor(self, ref: SystemMonitorAttrRef) -> int | float | str:
        return getattr(ref.fn()[ref.key][ref.index], ref.field)

    async def update(self, attr: Attribute[SystemMonitorAttrRef, DataTypeT]):
        attr.set(attr.datatype(self._get_sensor(attr.ref)))
        print(attr.get())
