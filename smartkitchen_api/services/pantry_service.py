from bson import ObjectId


def get_default_pantry_model(user_id: ObjectId, username: str):
    pantry_model = {
        'user_id': user_id,
        'username': username,
        'pantry': [
            {'category_value': 101, 'category_name': 'Candy', 'items': []},
            {'category_value': 102, 'category_name': 'Frozen', 'items': []},
            {'category_value': 103, 'category_name': 'Drinks', 'items': []},
            {'category_value': 104, 'category_name': 'Laundry', 'items': []},
            {
                'category_value': 105,
                'category_name': 'Meat and Fish',
                'items': [],
            },
            {
                'category_value': 106,
                'category_name': 'Dairy and Eggs',
                'items': [],
            },
            {
                'category_value': 107,
                'category_name': 'Grocery Products',
                'items': [],
            },
            {
                'category_value': 108,
                'category_name': 'Personal hygiene',
                'items': [],
            },
            {
                'category_value': 109,
                'category_name': 'Grains and Cereals',
                'items': [],
            },
            {
                'category_value': 110,
                'category_name': 'Cleaning materials',
                'items': [],
            },
            {
                'category_value': 111,
                'category_name': 'Fruits and vegetables',
                'items': [],
            },
            {
                'category_value': 112,
                'category_name': 'Condiments and Sauces',
                'items': [],
            },
            {
                'category_value': 113,
                'category_name': 'Pasta and Wheat Products',
                'items': [],
            },
            {
                'category_value': 114,
                'category_name': 'Breads and Bakery Products',
                'items': [],
            },
            {
                'category_value': 115,
                'category_name': 'Canned goods and preserves',
                'items': [],
            },
        ],
    }

    return pantry_model
