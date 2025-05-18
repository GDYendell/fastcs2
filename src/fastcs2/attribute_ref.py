from typing import TypeVar


class AttributeRef:
    pass


AttrRefT = TypeVar("AttrRefT", bound=AttributeRef)
