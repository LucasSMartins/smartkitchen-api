from smartkitchen_api.models.connection_options.connections import (
    DBConnectionHandler,
)
from smartkitchen_api.models.connection_options.mongo_db_config import (
    mongo_db_infos,
)
from smartkitchen_api.models.repository.collections import CollectionHandler


def open_connection(collection):
    db_handler = DBConnectionHandler()
    db_handler.connect_to_db(mongo_db_infos['DB_NAME'])
    db_connection = db_handler.get_db_connection()

    collection_repository = CollectionHandler(db_connection, collection)

    return collection_repository
