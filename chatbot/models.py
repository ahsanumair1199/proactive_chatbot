from django.db import models
from accounts.models import Account
import uuid


class Conversation(models.Mode):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.TextField()
    recipient = models.CharField(max_length=100)
    # image_url = models.FileField()
    # video_url = models.FileField()
    level = models.CharField(max_length=20)
    embeddings = models.TextField()

    def __str__(self):
        return self.user.name
