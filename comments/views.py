from rest_captcha.serializers import RestCaptchaSerializer
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment
from .serializers import CommentListSerializer, CommentCreateSerializer


class CommentApiView(APIView, PageNumberPagination):
    page_size = 25

    def get(self, request):
        comments = Comment.objects.all()
        results = self.paginate_queryset(comments, request, view=self)
        serializer = CommentListSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        captcha_data = request.data.get("captcha")
        if not RestCaptchaSerializer(data=captcha_data).is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={"message": "Invalid captcha"}
            )

        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
