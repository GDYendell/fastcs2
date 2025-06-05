from typing import TypeVar

DataTypeT = TypeVar("DataTypeT", bound=int | float | str, covariant=True)
type DataType = int | float | str
