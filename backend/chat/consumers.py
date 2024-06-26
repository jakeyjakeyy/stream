import json

from channels.generic.websocket import AsyncWebsocketConsumer

from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from asgiref.sync import sync_to_async
import logging

logger = logging.getLogger(__name__)


async def get_username(access):
    try:
        UntypedToken(access)
    except (InvalidToken, TokenError) as e:
        logger.error(f"Error: {e}")
        return None

    # Get the user from the token
    user = UntypedToken(access)
    user = await sync_to_async(JWTAuthentication().get_user)(user)
    return user.username


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        access = text_data_json["access"]
        if not message or not access:
            return

        username = await get_username(access)
        if username is None:
            return

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message", "message": message, "username": username},
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({"message": message, "username": username})
        )
