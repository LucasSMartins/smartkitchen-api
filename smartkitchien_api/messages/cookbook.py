class InformationCookbook:
    COOKBOOK_FOUND: dict = {
        'title': 'cookbook Retrieved Successfully',
        'msg': 'The cookbook was retrieved successfully.',
    }

    COOKBOOK_CREATED: dict = {
        'title': 'Item creation',
        'msg': 'The item was successfully added to the cookbook.',
    }

    COOKBOOK_NOT_FOUND: dict = {
        'title': 'cookbook Not Found',
        'msg': 'The cookbook with the provided ID was not found.',
        'loc': ['path', 'user_id'],
    }

    ITEM_NOT_FOUND: dict = {
        'title': 'Item Not Found',
        'msg': 'The specified item was not found in the category.',
        'loc': ['path', 'item_id'],
    }

    CATEGORY_NOT_FOUND: dict = {
        'title': 'Category Not Found',
        'msg': "The specified category was not found in the user's cookbook.",
        'loc': ['path', 'category_value'],
    }

    ITEM_DELETED: dict = {
        'title': 'Item deleted',
        'msg': 'Item successfully deleted from the category.',
    }
