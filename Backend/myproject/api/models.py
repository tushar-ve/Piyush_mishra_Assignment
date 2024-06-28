from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
User = get_user_model()

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.timestamp}'

class SentimentAnalysis(models.Model):
    chat_message = models.OneToOneField(ChatMessage, on_delete=models.CASCADE)
    sentiment_score = models.FloatField()

    def __str__(self):
        return f'Sentiment Analysis for {self.chat_message}'
    

class Chat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat by {self.user.username} at {self.timestamp}"