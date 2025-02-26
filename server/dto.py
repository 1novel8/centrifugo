import typing

from pydantic import BaseModel


class PublishMessageRequest(BaseModel):
    channel: str
    message: dict

##########################################
#           JWT Authentication


class AuthenticationTokenRequest(BaseModel):
    user_id: str


class SubscriptionTokenRequestDto(BaseModel):
    user_id: str
    channel: str


class TokenResponse(BaseModel):
    token: str

########################################
#        Connection Flow


class ConnectResult(BaseModel):
    user: str
    expire_at: int | None = None
    info: dict | None = None
    b64info: str | None = None
    b64data: str | None = None
    data: dict | None = None
    channels: list[str] | None = None
    subs: None = None
    meta: dict | None = None


class ConnectEventResponseDto(BaseModel):
    result: ConnectResult | None = None
    error: typing.Any = None
    disconnect: typing.Any = None


# ########################################
#        Subscribe Flow
class SubscribeEventRequestDto(BaseModel):
    client: str
    transport: str
    protocol: str
    encoding: str
    user: str
    channel: str


class ErrorDto(BaseModel):
    code: int
    message: str


class SubscribeEventResponse(BaseModel):
    result: typing.Any = None
    error: ErrorDto | None = None
    disconnect: typing.Any = None

#########################################
