from pydantic import BaseModel
from typing import List, Optional

# Esquema para un precio individual (usado para la creación y lectura)
class PriceBase(BaseModel):
    store: str
    price: float
    in_stock: bool
    url: str

class PriceCreate(PriceBase):
    pass

class Price(PriceBase):
    id: int
    game_id: int

    class Config:
        orm_mode = True

# Esquema para un juego (usado para la creación y lectura)
class GameBase(BaseModel):
    name: str

class GameCreate(GameBase):
    pass

class Game(GameBase):
    id: int
    prices: List[Price] = []

    class Config:
        orm_mode = True
