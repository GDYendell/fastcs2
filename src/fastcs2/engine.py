import asyncio
from functools import partial

from IPython.terminal.embed import InteractiveShellEmbed

from fastcs2.controller import Controller


async def interactive_shell(context: dict[str, object]):
    shell = InteractiveShellEmbed()
    await asyncio.to_thread(partial(shell.mainloop, local_ns=context))


class Engine:
    def __init__(self, loop: asyncio.AbstractEventLoop, controller: Controller) -> None:
        self._loop = loop
        self._controller = controller

    async def serve(self) -> None:
        await self._controller.initialise()
        update_tasks = self._controller.create_update_tasks()

        async def _scan():
            while True:
                await asyncio.gather(
                    asyncio.sleep(1), *[update() for update in update_tasks]
                )

        self._loop.create_task(_scan())

        self._loop.create_task(interactive_shell({"controller": self._controller}))

        while True:
            await asyncio.sleep(1)
