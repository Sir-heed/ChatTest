from django.db import models
from user.models import User

# Create your models here.
class Chat(models.Model):
    text = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='message_sender')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='message_receiver')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.id}"