from enum import Enum
from typing import List

from beanie import Document, PydanticObjectId
from bson import ObjectId
from pydantic import BaseModel, Field

"""
    **List of food category values**\n
    Candy = 101,\n
    Frozen = 102,\n
    Drinks = 103,\n
    Laundry = 104,\n
    Meat and Fish = 105,\n
    Dairy and Eggs = 106,\n
    Grocery Products = 107,\n
    Personal hygiene = 108,\n
    Grains and Cereals = 109,\n
    Cleaning materials = 110,\n
    Fruits and vegetables = 111,\n
    Condiments and Sauces = 112,\n
    Pasta and Wheat Products = 113,\n
    Breads and Bakery Products = 114,\n
    Canned goods and preserves = 115,\n
    Seasonings and Dried Herbs = 116.\n
    Stationery = 117\n
#     """


class CategoryValue(int, Enum):
    BREADS_BAKERY_PRODUCTS = 101
    CANDY = 102
    CANNED_GOODS_PRESERVES = 103
    CLEANING_MATERIALS = 104
    CONDIMENTS_SAUCES = 105
    DAIRY_EGGS = 106
    DRINKS = 107
    FROZEN = 108
    FRUITS_VEGETABLES = 109
    GRAINS_CEREALS = 110
    GROCERY_PRODUCTS = 111
    LAUNDRY = 112
    MEAT_FISH = 113
    PASTA_WHEAT_PRODUCTS = 114
    PERSONAL_HYGIENE = 115
    SEASONINGS_AND_DRIED_HERBS = 116
    STATIONERY = 117


class Units(str, Enum):
    UNITS = 'un'
    LITERS = 'l'
    MILLILITER = 'ml'
    GRAMS = 'g'
    KILO_GRAMS = 'kg'


class Items(BaseModel):
    id: str = Field(default=ObjectId())
    item_name: str = Field(
        ..., min_length=2, max_length=20, pattern=r'^([a-zA-Z0-9À-ÖØ-öø-ÿ -])+$'
    )
    quantity: int
    unit: Units

    # @field_validator('id')
    # def set_id(cls, value):
    #     return str(ObjectId()) if value is None else value


class Categories(BaseModel):
    category_value: CategoryValue
    category_name: str
    items: List[Items] = []


class Pantry(Document):
    user_id: PydanticObjectId
    pantry: dict[str, dict] = {}

    class Settings:
        name = 'pantry'


pantry_example = {'item_name': 'Coca-Cola', 'quantity': 2, 'unit': 'l'}
