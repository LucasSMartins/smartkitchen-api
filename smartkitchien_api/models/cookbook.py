from beanie import Document, PydanticObjectId
from pydantic import BaseModel

from smartkitchien_api.schema.categories import Categories


class Cookbook(Document):
    user_id: PydanticObjectId
    cookbook: list[Categories] = []

    class Settings:
        name = 'cookbook'
        keep_nulls = False


class CookbookPublic(BaseModel):
    cookbook: list[Categories]


recipe_example = {
    'name': 'Recipe Example',
    'preparation_time': '01:30',
    'ingredients': [
        {'name': 'string', 'quantity': 'string'},
        {'name': 'string', 'quantity': 'string'},
    ],
    'method_preparation': 'String',
    'portion': 4,
}
