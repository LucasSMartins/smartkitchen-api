from enum import Enum
from typing import List

from beanie import DecimalAnnotation, Document, PydanticObjectId
from bson import ObjectId
from pydantic import BaseModel, Field


class CategoryValue(Enum):
    BREADS_BAKERY_PRODUCTS = '101'
    CANDY = '102'
    CANNED_GOODS_PRESERVES = '103'
    CLEANING_MATERIALS = '104'
    CONDIMENTS_SAUCES = '105'
    DAIRY_EGGS = '106'
    DRINKS = '107'
    FROZEN = '108'
    FRUITS_VEGETABLES = '109'
    GRAINS_CEREALS = '110'
    GROCERY_PRODUCTS = '111'
    LAUNDRY = '112'
    MEAT_FISH = '113'
    PASTA_WHEAT_PRODUCTS = '114'
    PERSONAL_HYGIENE = '115'
    SEASONINGS_AND_DRIED_HERBS = '116'
    STATIONERY = '117'


class Units(Enum):
    UNITS = 'un'
    LITERS = 'l'
    MILLILITER = 'ml'
    GRAMS = 'g'
    KILO_GRAMS = 'kg'


class Items(BaseModel):
    id: PydanticObjectId = Field(default=ObjectId())
    item_name: str = Field(
        ..., min_length=2, max_length=20, pattern=r'^([a-zA-Z0-9À-ÖØ-öø-ÿ -])+$'
    )
    quantity: int
    unit: Units
    price: DecimalAnnotation | None = None


class ItemsUpdate(BaseModel):
    id: PydanticObjectId | None = None
    item_name: str | None = Field(
        None, min_length=2, max_length=20, pattern=r'^([a-zA-Z0-9À-ÖØ-öø-ÿ -])+$'
    )
    quantity: int | None = None
    unit: Units | None = None
    price: DecimalAnnotation | None = None


class Categories(BaseModel):
    category_value: CategoryValue
    category_name: str
    items: List[Items] = []


class ShoppingCart(Document):
    user_id: PydanticObjectId
    shopping_cart: list[Categories]

    class Settings:
        name = 'shopping_cart'


class ShoppingCartPublic(BaseModel):
    shopping_cart: list[Categories]


item_example = {'item_name': 'Coca-Cola', 'quantity': 2, 'unit': 'l', 'price': 3.23}
