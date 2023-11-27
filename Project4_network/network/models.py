from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "body": self.text,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }

class Follow(models.Model):
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="follower", null=True)
    followee = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followee", null=True)

    def serialize(self):
        return {
            "id": self.id,
            "follower": self.follower,
            "followee": self.followee
        }

class Like(models.Model):
    liked_post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post")
    liker = models.ForeignKey("User", on_delete=models.CASCADE, related_name="liker", null=True)

    def serialize(self):
        return {
            "id": self.id,
            "liked_post": self.liked_post,
            "liker": self.liker
        }


