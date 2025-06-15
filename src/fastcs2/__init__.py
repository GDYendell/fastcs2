"""Top level API.

.. data:: __version__
    :type: str

    Version number as calculated by https://github.com/pypa/setuptools_scm
"""

from ._version import __version__ as __version__
from .attribute import AttributeR as AttributeR
from .attribute import AttributeRW as AttributeRW
from .attribute import AttributeW as AttributeW
from .attribute_io import AttributeIO as AttributeIO
from .attribute_io_ref import AttributeIORef as AttributeIORef
from .control_system import FastCS as FastCS
from .controller import Controller as Controller
from .datatypes import DataType as DataType
from .transport import ConsoleTransport as ConsoleTransport
