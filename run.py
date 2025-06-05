import asyncio

from fastcs2.demo.controller import SystemMonitorController
from fastcs2.engine import Engine

loop = asyncio.new_event_loop()
controller = SystemMonitorController()
engine = Engine(loop, controller)

loop.run_until_complete(engine.serve())
