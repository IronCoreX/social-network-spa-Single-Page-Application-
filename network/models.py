from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # Hint: We can also track likes directly or via a separate model
    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts")

    def __str__(self):
        return f"Post {self.id} by {self.user} at {self.timestamp}"

class Follow(models.Model):
    # User who is following someone
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    # User who is being followed
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.user} follows {self.followed_user}"