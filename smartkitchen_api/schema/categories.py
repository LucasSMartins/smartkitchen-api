from pydantic import BaseModel

from smartkitchen_api.schema.enums.category_value import CategoryValue
from smartkitchen_api.schema.items import Items
from smartkitchen_api.schema.recipe import Recipe


class Categories(BaseModel):
    category_value: CategoryValue
    category_name: str
    items: list[Items | Recipe] = []
