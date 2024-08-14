from pydantic import BaseModel


class InformationShoppingCart(BaseModel):
    CART_FOUND: dict = {
        'title': 'Shopping Cart Retrieved Successfully',
        'msg': 'The shopping cart was retrieved successfully.',
    }
    CART_CREATED: dict = {
        'title': 'Item creation',
        'msg': 'The item was successfully added to the shopping cart.',
    }
    CART_NOT_FOUND: dict = {
        'title': 'Shopping Cart Not Found',
        'msg': 'The shopping cart with the provided ID was not found.',
        'loc': ['path', 'user_id'],
    }

    CATEGORY_NOT_FOUND: dict = {
        'title': 'Category Not Found',
        'msg': "The specified category was not found in the user's shopping cart.",
        'loc': ['path', 'category_value'],
    }

    ITEM_NOT_FOUND: dict = {
        'title': 'Item Not Found',
        'msg': 'The specified item was not found in the shopping cart.',
        'loc': ['path', 'item_id'],
    }
    ITEM_DELETED: dict = {
        'title': 'Item deleted',
        'msg': 'Item successfully deleted from the shopping cart.',
    }
    ITEM_UPDATED: dict = {
        'title': 'Item updated',
        'msg': 'Item successfully updated in the shopping cart.',
    }
    ITEM_ADDED: dict = {
        'title': 'Item added',
        'msg': 'Item successfully added to the shopping cart.',
    }

    ITEM_ALREADY_EXISTS: dict = {
        'title': 'Item Already Exists',
        'msg': 'The item with the same name already exists in the category.',
        'loc': ['body', 'name'],
    }
