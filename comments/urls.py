from django.urls import path

from comments.views import CommentApiView

urlpatterns = [
    path("", CommentApiView.as_view())
]

app_name = "comments"
