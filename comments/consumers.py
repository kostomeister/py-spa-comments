from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_captcha.serializers import RestCaptchaSerializer
from rest_framework.exceptions import ValidationError
from .models import Comment
from .serializers import CommentListSerializer, CommentCreateSerializer
import json


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'comments'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')
        data = text_data_json.get('data', {})

        if action == 'list':
            comments = await self.get_comments()
            await self.send(text_data=json.dumps(comments))
        elif action == 'create':
            captcha_data = data.get("captcha")
            if not RestCaptchaSerializer(data=captcha_data).is_valid():
                await self.send(text_data=json.dumps({"non_field_errors": ["Invalid captcha"]}))
                return
            try:
                comment = await self.create_comment(data)
                await self.send(text_data=json.dumps(comment))
            except ValidationError as e:
                await self.send(text_data=json.dumps(e.detail))
        else:
            await self.send(text_data=json.dumps({"non_field_errors": ["Error"]}))

    async def get_comments(self, page=1):
        page_size = 25
        start_index = (page - 1) * page_size
        end_index = start_index + page_size

        comments = await self.fetch_comments(start_index, end_index)
        serialized_comments = await self.serialize_comments(comments)
        return serialized_comments

    @database_sync_to_async
    def fetch_comments(self, start_index, end_index):
        comments = Comment.objects.all()[start_index:end_index]
        return comments

    @database_sync_to_async
    def serialize_comments(self, comments):
        serializer = CommentListSerializer(comments, many=True)
        return serializer.data

    @database_sync_to_async
    def create_comment(self, data):
        serializer = CommentCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        return CommentListSerializer(comment).data
