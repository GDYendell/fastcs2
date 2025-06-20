from typing import TypeVar

DataTypeT = TypeVar("DataTypeT", bound=int | float | str, covariant=True)
DataTypeInT = TypeVar("DataTypeInT", bound=int | float | str, contravariant=True)
DataType = int | float | str
