from pydantic import BaseModel
from typing import Optional


class CountryBase(BaseModel):
    name: str


class CountryCreate(CountryBase):
    pass


class CountryUpdate(CountryBase):
    pass


class Country(CountryBase):
    id: int

    class Config:
        orm_mode = True


class PlayerBase(BaseModel):
    first_name: str
    last_name: str
    country_born_id: Optional[int]
    country_nationality_id: Optional[int]
    current_club_id: Optional[int]
    position_id: Optional[int]
    sub_position: Optional[str]
    foot: Optional[str]
    height_in_cm: Optional[int]
    image_url: Optional[str]
    retired: bool = False


class PlayerCreate(PlayerBase):
    pass


class PlayerUpdate(PlayerBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    retired: Optional[bool] = None


class Player(PlayerBase):
    id_player: int

    class Config:
        orm_mode = True
