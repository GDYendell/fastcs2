from fastcs2 import ConsoleTransport, FastCS
from fastcs2.demo.controller import SystemMonitorController

controller = SystemMonitorController()
fastcs = FastCS(controller, ConsoleTransport)

fastcs.run()
