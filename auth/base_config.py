# Cookie for transporting user's token (For authentication)
# JWT for storing user's token
from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend
from config import SECRET
from fastapi_users import FastAPIUsers
from auth.models import User
from auth.manager import get_user_manager

cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()