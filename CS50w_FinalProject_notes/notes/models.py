from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Note(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    position = models.IntegerField(null = True, blank = True)
    color = models.TextField(blank = True, null = True)

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "text": self.text,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "position": self.position,
            "color": self.color
        }
