from collections import defaultdict
from collections.abc import Callable, Coroutine, Sequence
from functools import partial

from fastcs2.attribute import AnyAttribute, AttributeR, AttributeRW, AttributeW
from fastcs2.attribute_io import AnyAttributeIO
from fastcs2.attribute_io_ref import AttributeIORef
from fastcs2.controller_api import ControllerAPI


class Controller:
    def __init__(self, attribute_io: AnyAttributeIO | Sequence[AnyAttributeIO]):
        if not isinstance(attribute_io, Sequence):
            attribute_io = [attribute_io]

        self._attribute_ref_io_map = {io.ref: io for io in attribute_io}
        self._attributes: dict[str, AnyAttribute] = {}

        self.path: list[str] = []
        self._sub_controllers: dict[str, Controller] = {}

        self._bind_attrs()

    def add_attribute(self, attribute: AnyAttribute):
        self._attributes[attribute.name] = attribute

    def _bind_attrs(self):
        for attribute_name in dir(self):
            if attribute_name.startswith("_"):
                continue

            attribute = getattr(self, attribute_name)
            if isinstance(attribute, AttributeR | AttributeW):
                io_ref_cls = type(attribute.io_ref)  # type: ignore

                if io_ref_cls == AttributeIORef:
                    continue

                assert issubclass(io_ref_cls, AttributeIORef)

                self.add_attribute(attribute)  # type: ignore

    async def initialise(self):
        pass

    async def post_initialise(self):
        for attribute in self._attributes.values():
            assert attribute.io_ref.__class__ in self._attribute_ref_io_map.keys(), (
                f"{self.__class__.__name__} does not have an AttributeIO to handle "
                f"{attribute.io_ref.__class__.__name__}"
            )

        for sub_controller in self._sub_controllers.values():
            await sub_controller.post_initialise()

        self._link_attr_put_send_callbacks()

    def create_update_tasks(
        self,
    ) -> dict[float, list[Callable[[], Coroutine[None, None, None]]]]:
        update_tasks: dict[float, list[Callable[[], Coroutine[None, None, None]]]] = (
            defaultdict(list)
        )
        for attribute in self._attributes.values():
            if isinstance(attribute, AttributeR) and attribute.io_ref.update_period:
                update_tasks[attribute.io_ref.update_period].append(
                    partial(
                        self._attribute_ref_io_map[type(attribute.io_ref)].update,
                        attribute,
                    )
                )

        for sub_controller in self._sub_controllers.values():
            for period, updates in sub_controller.create_update_tasks().items():
                update_tasks[period].extend(updates)

        return update_tasks

    def _link_attr_put_send_callbacks(self):
        for attribute in self._attributes.values():
            if isinstance(attribute, AttributeRW):
                attribute.put_callbacks.append(
                    self._attribute_ref_io_map[type(attribute.io_ref)].send
                )

    def register_sub_controller(self, name: str, controller: "Controller"):
        if name in self._sub_controllers:
            raise ValueError(f"Controller already has a subcontroller under {name}")
        if controller.path:
            raise ValueError("Controller already registered at path {controller._path}")

        controller.path = self.path + [name]
        self._sub_controllers[name] = controller

    def build_api(self) -> ControllerAPI:
        return ControllerAPI(
            self.path,
            self._attributes,
            {
                name: controller.build_api()
                for name, controller in self._sub_controllers.items()
            },
        )
