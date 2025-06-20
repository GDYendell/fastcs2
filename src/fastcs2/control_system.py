import asyncio
from collections.abc import Callable, Coroutine
from functools import partial

from IPython.terminal.embed import InteractiveShellEmbed

from fastcs2.controller import Controller
from fastcs2.transport import Transport


async def interactive_shell(context: dict[str, object], stop_event: asyncio.Event):
    shell = InteractiveShellEmbed()
    await asyncio.to_thread(partial(shell.mainloop, local_ns=context))

    stop_event.set()


class FastCS:
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        controller: Controller,
        transports: list[type[Transport]],
    ) -> None:
        self._loop = loop
        self._controller = controller
        self._transports = transports

    async def serve(self) -> None:
        await self._controller.initialise()
        await self._controller.post_initialise()

        update_tasks = self._controller.create_update_tasks()

        api = self._controller.build_api()

        for update_period, updates in update_tasks.items():

            async def _scan(
                _period: float = update_period,
                _updates: list[Callable[[], Coroutine[None, None, None]]] = updates,
            ):
                while True:
                    await asyncio.gather(
                        asyncio.sleep(_period),
                        *[update() for update in _updates],
                    )

            self._loop.create_task(_scan())

        for transport in self._transports:
            transport(api)

        stop_event = asyncio.Event()

        def run(coro: Coroutine[None, None, None]):
            """Run coroutine on FastCS event loop from IPython thread."""

            def wrapper():
                asyncio.create_task(coro)

            self._loop.call_soon_threadsafe(wrapper)

        self._loop.create_task(
            interactive_shell({"controller": self._controller, "run": run}, stop_event)
        )

        await stop_event.wait()
