from django.core.validators import RegexValidator
from django.db import models


class Comment(models.Model):
    username = models.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex="^[a-zA-Z0-9]*$",
                message="Username must be Alphanumeric",
                code="invalid_username",
            ),
        ],
    )
    email = models.EmailField()
    text = models.TextField()
    home_page = models.URLField(blank=True, null=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Id: {self.id}; user: {self.username}; created_at: {self.created_at}"
