from django.db import models
from accounts.models import WhatsappUser
import uuid
from pgvector.django import VectorField


class AddMessage(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    message = models.TextField()
    image_url = models.CharField(max_length=255, blank=True)
    video_url = models.CharField(max_length=255, blank=True)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class Conversation(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    whatsapp_user = models.ForeignKey(WhatsappUser, on_delete=models.CASCADE)
    sender = models.CharField(max_length=50, blank=False)
    receiver = models.CharField(max_length=50, blank=False)
    text = models.TextField()
    image_url = models.CharField(max_length=255, blank=True)
    video_url = models.CharField(max_length=255, blank=True)
    level = models.CharField(max_length=30, blank=True)
    embedding = VectorField(dimensions=3, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.whatsapp_user.name


class GptResponse(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    whatsapp_user = models.ForeignKey(WhatsappUser, on_delete=models.CASCADE)
    text = models.TextField()
    embedding = VectorField(dimensions=3)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.whatsapp_user.name


# class ErrorLog(models.Model):
#     error_name = models.CharField(max_length=255)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.error_name
