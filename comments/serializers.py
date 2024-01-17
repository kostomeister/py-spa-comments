from rest_captcha.serializers import RestCaptchaSerializer
from rest_framework import serializers

from comments.models import Comment


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentCreateSerializer(serializers.ModelSerializer):
    captcha = RestCaptchaSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["username", "email", "text", "home_page", "parent", "captcha"]
