import asyncio

from fastcs2.demo.controller import SystemMonitorController
from fastcs2.engine import Engine
from fastcs2.transport import LogTransport

loop = asyncio.new_event_loop()
controller = SystemMonitorController()
engine = Engine(loop, controller, [LogTransport])

loop.run_until_complete(engine.serve())
