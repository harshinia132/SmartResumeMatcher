from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Job(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.JSONField(default=list, blank=True)
    embedding = models.BinaryField(null=True, blank=True)  # ✅ BinaryField for pickle data
    #created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title