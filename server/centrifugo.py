import datetime
import typing

import jwt
from cent import AsyncClient, PublishRequest, PublishResult
from pydantic import BaseModel

API_URL = "http://localhost:8000/api"
HMAC_SECRET = "hmac_secret_key"  # for client jwt
API_KEY = "http_api_key"


class JWTClaims(BaseModel):
    sub: str | None = None
    exp: int | None = None
    channel: str | None = None


class Centrifugo:
    def __init__(self):
        self.api_url = API_URL
        self.api_key = API_KEY

    @staticmethod
    def get_authentication_token(user_id: str | int) -> str:
        jwt_claims = JWTClaims(
            sub=str(user_id),
            exp=int((datetime.datetime.now() + datetime.timedelta(hours=4, minutes=10)).timestamp()),
        )
        return jwt.encode(jwt_claims.model_dump(exclude_unset=True), HMAC_SECRET, algorithm="HS256")

    @staticmethod
    def get_subscription_token(user_id: str | int, channel: str) -> str:
        jwt_claims = JWTClaims(
            sub=str(user_id),
            exp=int((datetime.datetime.now() + datetime.timedelta(hours=4, minutes=10)).timestamp()),
            channel=channel
        )
        return jwt.encode(jwt_claims.model_dump(), HMAC_SECRET, algorithm="HS256")

    async def publish_message(self, message: typing.Any, channel: str) -> PublishResult:
        request = PublishRequest(channel=channel, data=message)
        result = await self.async_client.publish(request=request)
        return result

    @property
    def async_client(self) -> AsyncClient:
        return AsyncClient(api_url=self.api_url, api_key=self.api_key)
