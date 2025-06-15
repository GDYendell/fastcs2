import asyncio
from functools import partial

from IPython.terminal.embed import InteractiveShellEmbed

from fastcs2.controller import Controller
from fastcs2.transport import Transport


async def interactive_shell(context: dict[str, object], stop_event: asyncio.Event):
    shell = InteractiveShellEmbed()
    await asyncio.to_thread(partial(shell.mainloop, local_ns=context))

    stop_event.set()


class Engine:
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
        update_tasks = self._controller.create_update_tasks()

        api = self._controller.build_api()

        async def _scan():
            while True:
                await asyncio.gather(
                    asyncio.sleep(1), *[update() for update in update_tasks]
                )

        self._loop.create_task(_scan())

        for transport in self._transports:
            transport(api)

        stop_event = asyncio.Event()

        self._loop.create_task(
            interactive_shell({"controller": self._controller}, stop_event)
        )

        await stop_event.wait()
