from enum import Enum
from typing import List

from beanie import Document, PydanticObjectId
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
#     """


class CategoryValue(int, Enum):
    CANDY = 101
    FROZEN = 102
    DRINKS = 103
    LAUNDRY = 104
    MEAT_FISH = 105
    DAIRY_EGGS = 106
    GROCERY_PRODUCTS = 107
    PERSONAL_HYGIENE = 108
    GRAINS_CEREALS = 109
    CLEANING_MATERIALS = 110
    FRUITS_VEGETABLES = 111
    CONDIMENTS_SAUCES = 112
    PASTA_WHEAT_PRODUCTS = 113
    BREADS_BAKERY_PRODUCTS = 114
    CANNED_GOODS_PRESERVES = 115


class Units(str, Enum):
    UNITS = 'un'
    LITERS = 'l'
    MILLILITER = 'ml'
    GRAMS = 'g'
    KILO_GRAMS = 'kg'


class ItemsOut(BaseModel):
    item_id: PydanticObjectId
    item_name: str
    quantity: int
    unit: Units


class ItemsIn(BaseModel):
    item_name: str = Field(
        ..., min_length=2, max_length=15, pattern=r'^([a-zA-Z0-9À-ÖØ-öø-ÿ ])+$'
    )
    quantity: int
    unit: Units


class Categories(BaseModel):
    category_value: CategoryValue
    category_name: str
    items: List[ItemsOut] = []


class Pantry(Document):
    user_id: PydanticObjectId
    username: str
    pantry: List[Categories]

    class Settings:
        name = 'pantry'


pantry_data = [
    {'category_value': CategoryValue.CANDY, 'category_name': 'Candy', 'items': []},
    {'category_value': CategoryValue.FROZEN, 'category_name': 'Frozen', 'items': []},
    {'category_value': CategoryValue.DRINKS, 'category_name': 'Drinks', 'items': []},
    {'category_value': CategoryValue.LAUNDRY, 'category_name': 'Laundry', 'items': []},
    {
        'category_value': CategoryValue.MEAT_FISH,
        'category_name': 'Meat and Fish',
        'items': [],
    },
    {
        'category_value': CategoryValue.DAIRY_EGGS,
        'category_name': 'Dairy and Eggs',
        'items': [],
    },
    {
        'category_value': CategoryValue.GROCERY_PRODUCTS,
        'category_name': 'Grocery Products',
        'items': [],
    },
    {
        'category_value': CategoryValue.PERSONAL_HYGIENE,
        'category_name': 'Personal hygiene',
        'items': [],
    },
    {
        'category_value': CategoryValue.GRAINS_CEREALS,
        'category_name': 'Grains and Cereals',
        'items': [],
    },
    {
        'category_value': CategoryValue.CLEANING_MATERIALS,
        'category_name': 'Cleaning materials',
        'items': [],
    },
    {
        'category_value': CategoryValue.FRUITS_VEGETABLES,
        'category_name': 'Fruits and vegetables',
        'items': [],
    },
    {
        'category_value': CategoryValue.CONDIMENTS_SAUCES,
        'category_name': 'Condiments and Sauces',
        'items': [],
    },
    {
        'category_value': CategoryValue.PASTA_WHEAT_PRODUCTS,
        'category_name': 'Pasta and Wheat Products',
        'items': [],
    },
    {
        'category_value': CategoryValue.BREADS_BAKERY_PRODUCTS,
        'category_name': 'Breads and Bakery Products',
        'items': [],
    },
    {
        'category_value': CategoryValue.CANNED_GOODS_PRESERVES,
        'category_name': 'Canned goods and preserves',
        'items': [],
    },
]
