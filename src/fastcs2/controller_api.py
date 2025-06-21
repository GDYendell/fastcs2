from collections.abc import Iterator
from dataclasses import dataclass, field

from fastcs2.attribute import AnyAttribute


@dataclass(frozen=True)
class ControllerAPI:
    path: list[str]
    attributes: dict[str, AnyAttribute]
    sub_controllers: dict[str, "ControllerAPI"] = field(
        default_factory=dict[str, "ControllerAPI"]
    )

    def walk_controllers(self) -> Iterator["ControllerAPI"]:
        yield self

        for sub_controller in self.sub_controllers.values():
            yield from sub_controller.walk_controllers()

    def walk_attributes(self) -> Iterator[AnyAttribute]:
        yield from self.attributes.values()

        for sub_controller in self.sub_controllers.values():
            yield from sub_controller.walk_attributes()
