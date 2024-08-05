from beanie import PydanticObjectId
from bson import ObjectId
from pydantic import BaseModel, Field, conlist, constr


class Ingredients(BaseModel):
    id: PydanticObjectId = Field(default_factory=ObjectId)
    name: constr(min_length=1) = Field(...)  # type: ignore
    quantity: constr(min_length=1) = Field(...)  # type: ignore


class Recipe(BaseModel):
    id: PydanticObjectId = Field(default_factory=ObjectId)
    name: constr(min_length=1) = Field(...)  # type: ignore
    preparation_time: constr(pattern=r'^\d{2}:\d{2}$') = Field(  # type: ignore
        ..., description='Tempo de preparo no formato HH:MM'
    )
    ingredients: conlist(Ingredients, min_length=1) = Field(...)  # type: ignore
    method_preparation: constr(min_length=1) = Field(...)  # type: ignore
    portion: int = Field(..., gt=0)
