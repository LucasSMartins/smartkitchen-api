from smartkitchen_api.models.user import User


class FakerUser(User):
    clean_password: str
