import asyncio
from collections.abc import Callable, Coroutine
from functools import partial

from fastcs2.attribute import Attribute
from fastcs2.controller import Controller


class Engine:
    def __init__(self, loop: asyncio.AbstractEventLoop, controller: Controller) -> None:
        self._loop = loop
        self._controller = controller

    async def serve(self) -> None:
        updates: list[Callable[[], Coroutine[None, None, None]]] = []
        for attribute_name in dir(self._controller):
            if attribute_name.startswith("_"):
                continue

            attribute = getattr(self._controller, attribute_name)
            if isinstance(attribute, Attribute):
                updates.append(
                    partial(
                        self._controller.io[attribute.ref.__class__].update, attribute
                    )
                )
                self._controller.attributes.append(attribute)

        for attribute in self._controller.attributes:
            await self._controller.io[attribute.ref.__class__].initialise(
                attribute, self._controller.attributes
            )

        async def _scan():
            while True:
                await asyncio.gather(
                    asyncio.sleep(1), *[update() for update in updates]
                )

        self._loop.create_task(_scan())

        while True:
            await asyncio.sleep(1)
