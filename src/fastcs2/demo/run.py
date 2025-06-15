import asyncio

from fastcs2 import ConsoleTransport, FastCS
from fastcs2.demo.controller import SystemMonitorController

loop = asyncio.new_event_loop()
controller = SystemMonitorController()
engine = FastCS(loop, controller, [ConsoleTransport])

loop.run_until_complete(engine.serve())
