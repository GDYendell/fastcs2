import asyncio
from collections.abc import Callable, Coroutine
from functools import partial
from typing import Any

from IPython.terminal.embed import InteractiveShellEmbed

from fastcs2.controller import Controller
from fastcs2.transport import Transport


class FastCS:
    def __init__(
        self,
        controller: Controller,
        transport: type[Transport] | list[type[Transport]],
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        self._controller = controller
        self._transports = transport if isinstance(transport, list) else [transport]
        self._loop = loop or asyncio.new_event_loop()

    async def serve(self) -> None:
        await self._controller.initialise()
        await self._controller.post_initialise()

        update_tasks = self._controller.create_update_tasks()
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

        api = self._controller.build_api()

        context: dict[str, Any] = {"controller": self._controller}
        for transport_cls in self._transports:
            # TODO: Register transports with key and use as prefix to avoid conflicts
            transport = transport_cls(api)
            context.update(transport.context)

        await self._interactive_shell(context)

    async def _interactive_shell(self, context: dict[str, Any]):
        """Spawn interactive shell in another thread and wait for it to complete."""

        def run(coro: Coroutine[None, None, None]):
            """Run coroutine on FastCS event loop from IPython thread."""

            def wrapper():
                asyncio.create_task(coro)

            self._loop.call_soon_threadsafe(wrapper)

        async def interactive_shell(
            context: dict[str, object], stop_event: asyncio.Event
        ):
            """Run interactive shell in a new thread."""
            shell = InteractiveShellEmbed()
            await asyncio.to_thread(partial(shell.mainloop, local_ns=context))

            stop_event.set()

        context["run"] = run

        stop_event = asyncio.Event()
        self._loop.create_task(interactive_shell(context, stop_event))
        await stop_event.wait()

    def run(self) -> None:
        self._loop.run_until_complete(self.serve())
