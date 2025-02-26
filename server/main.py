from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from centrifugo import Centrifugo
from dto import TokenResponse, PublishMessageRequest, AuthenticationTokenRequest, \
    SubscriptionTokenRequestDto, ConnectEventResponseDto, ConnectResult, SubscribeEventRequestDto, \
    SubscribeEventResponse, ErrorDto

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.post("/token")
async def jwt_token(authentication_token_request_dto: AuthenticationTokenRequest) -> TokenResponse:
    auth_token = Centrifugo().get_authentication_token(user_id=authentication_token_request_dto.user_id)
    return TokenResponse(token=auth_token)


@app.post("/subscription/token")
async def get_subscription_token(subscription_token_request_dto: SubscriptionTokenRequestDto) -> TokenResponse:
    """ Здесь мы можем проверять пермишены перед тем как отдать токен """

    subscription_token = Centrifugo().get_authentication_token(
        user_id=subscription_token_request_dto.user_id
    )
    return TokenResponse(token=subscription_token)


@app.post("/publish")
async def publish_message(request: PublishMessageRequest):
    result = await Centrifugo().publish_message(channel=request.channel, message=request.message)
    return result


@app.post("/events/connection")
async def connection_event(
    user_id: int = 123,
) -> ConnectEventResponseDto:
    return ConnectEventResponseDto(
        result=ConnectResult(user=str(user_id))
    )


@app.post("/events/subscribe")
async def subscribe_event(
    subscribe_event_request_dto: SubscribeEventRequestDto,
) -> SubscribeEventResponse:
    """ Здесь мы можем проверять пермишены перед тем как разрешать подключение """
    namespace, channel = subscribe_event_request_dto.channel.split(':')
    if namespace == 'boys':
        if int(channel) % 2 == 0:
            return SubscribeEventResponse()
    elif namespace == 'girls':
        if int(channel) % 2 == 1:
            return SubscribeEventResponse()
    return SubscribeEventResponse(error=ErrorDto(code=4501, message='You are looser without permission'))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=5005, reload=True)
