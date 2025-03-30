from fastapi_oauth2.client import OAuth2Client
from fastapi_oauth2.config import OAuth2Config
from social_core.backends.yandex import YaruOAuth2

from src.config.settings import settings


yandex_client = OAuth2Client(
    backend=YaruOAuth2,
    client_id=settings.OAUTH2_YANDEX_CLIENT_ID,
    client_secret=settings.OAUTH2_YANDEX_CLIENT_SECRET,
    # redirect_uri="http://0.0.0.0:80/",
    scope=["login:email", "login:info"],
)


oauth2_config = OAuth2Config(
    allow_http=True,
    jwt_secret=settings.JWT_SECRET,
    jwt_expires=settings.JWT_EXPIRES,
    jwt_algorithm=settings.JWT_ALGORITHM,
    clients=[
        yandex_client,
    ]
)
