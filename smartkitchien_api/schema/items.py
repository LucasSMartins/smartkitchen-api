from beanie import DecimalAnnotation, PydanticObjectId
from bson import ObjectId
from pydantic import BaseModel, Field

from smartkitchien_api.schema.enums.units import Units


class Items(BaseModel):
    id: PydanticObjectId = Field(default_factory=ObjectId)
    name: str = Field(
        ..., min_length=2, max_length=20, pattern=r'^([a-zA-Z0-9À-ÖØ-öø-ÿ -])+$'
    )
    quantity: int
    unit: Units
    price: DecimalAnnotation | None = None


class ItemsUpdate(BaseModel):
    id: PydanticObjectId | None = None
    name: str | None = Field(
        None, min_length=2, max_length=20, pattern=r'^([a-zA-Z0-9À-ÖØ-öø-ÿ -])+$'
    )
    quantity: int | None = None
    unit: Units | None = None
    price: DecimalAnnotation | None = None
