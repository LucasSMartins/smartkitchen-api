from beanie import DecimalAnnotation, PydanticObjectId
from bson import ObjectId
from pydantic import BaseModel, Field

from smartkitchen_api.schema.enums.units import Units


class Items(BaseModel):
    id: PydanticObjectId = Field(default_factory=ObjectId)
    name: str = Field(
        ..., min_length=2, max_length=20, pattern=r'^([a-zA-Z0-9À-ÖØ-öø-ÿ -])+$'
    )
    quantity: int
    unit: Units
    price: DecimalAnnotation = Field(None, ge=0)


class ItemsUpdate(BaseModel):
    id: PydanticObjectId | None = None
    name: str | None = Field(
        None, min_length=2, max_length=20, pattern=r'^([a-zA-Z0-9À-ÖØ-öø-ÿ -])+$'
    )
    quantity: int | None = None
    unit: Units | None = None
    price: DecimalAnnotation = Field(None, ge=0)


class ItemsUpdateRecipe(BaseModel):
    name: str
    preparation_time: str
    ingredients: list[dict[str, str]]
    method_preparation: str
    portion: int
