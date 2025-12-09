from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    text = models.TextField(blank=True)
    skills = models.JSONField(default=list, blank=True)
    embedding = models.BinaryField(null=True, blank=True)  # ✅ BinaryField for pickle data
    #created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume {self.id} - {self.user.username}"