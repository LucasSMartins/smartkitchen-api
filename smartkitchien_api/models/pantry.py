from beanie import Document, PydanticObjectId
from pydantic import BaseModel

from smartkitchien_api.schema.categories import Categories


class Pantry(Document):
    user_id: PydanticObjectId
    pantry: list[Categories]

    class Settings:
        name = 'pantry'
        keep_nulls = False


class PantryPublic(BaseModel):
    pantry: list[Categories]


item_with_price = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}
item_without_price = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un'}

item_description = 'O campo "price" é opcional'
