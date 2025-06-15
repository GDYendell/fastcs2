from typing import TypeVar


class AttributeIORef:
    pass


AttributeIORefT = TypeVar("AttributeIORefT", bound=AttributeIORef, covariant=True)
