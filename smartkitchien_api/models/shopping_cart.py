from beanie import Document, PydanticObjectId
from pydantic import BaseModel

from smartkitchien_api.schema.categories import Categories


class ShoppingCart(Document):
    user_id: PydanticObjectId
    shopping_cart: list[Categories]

    class Settings:
        name = 'shopping_cart'
        keep_nulls = False


class ShoppingCartPublic(BaseModel):
    shopping_cart: list[Categories]


item_with_price = {'name': 'Coca-Cola', 'quantity': 2, 'unit': 'l', 'price': 14.00}
item_without_price = {'name': 'Trakinas', 'quantity': 1, 'unit': 'un'}

item_description = 'O campo "price" é opcional'
