
    
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):  # This should be 'User' not 'CustomUser'
    is_candidate = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username