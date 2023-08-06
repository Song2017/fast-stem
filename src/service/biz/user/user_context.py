from src.core import Context


class UserContext(Context):
    """
    User Context, service cache
    """
    _redis_auth_name = "CBEC_USER_AUTH"
