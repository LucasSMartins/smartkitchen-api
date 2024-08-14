from pydantic import BaseModel


class InformationPantry(BaseModel):
    PANTRY_FOUND: dict = {
        'title': 'Pantry Retrieved Successfully',
        'msg': 'The pantry was retrieved successfully.',
    }

    PANTRY_CREATED: dict = {
        'title': 'Item creation',
        'msg': 'The item was successfully added to the pantry.',
    }

    PANTRY_NOT_FOUND: dict = {
        'title': 'Pantry Not Found',
        'msg': 'The pantry with the provided ID was not found.',
        'loc': ['path', 'user_id'],
    }

    ITEM_ALREADY_EXISTS: dict = {
        'title': 'Item Already Exists',
        'msg': 'An item with the same name already exists in this category.',
        'loc': ['body', 'name'],
    }

    ITEM_NOT_FOUND: dict = {
        'title': 'Item Not Found',
        'msg': 'The specified item was not found in the category.',
        'loc': ['path', 'item_id'],
    }

    CATEGORY_NOT_FOUND: dict = {
        'title': 'Category Not Found',
        'msg': "The specified category was not found in the user's pantry.",
        'loc': ['path', 'category_value'],
    }

    ITEM_DELETED: dict = {
        'title': 'Item deleted',
        'msg': 'Item successfully deleted from the category.',
    }
