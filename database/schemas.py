from typing import Union
from pydantic import BaseModel

from .enums import IncentiveType


class Product(BaseModel):
    id: int
    brand_id: int
    name: str
    efficiency: Union[float, None]
    diameter: Union[float, None]
    height: Union[float, None]
    width: Union[float, None]
    type: IncentiveType

    class Config:
        orm_mode = True


class Brand(BaseModel):
    id: int
    name: str
    website: str
    products: list[Product] = []

    class Config:
        orm_mode = True
