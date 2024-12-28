from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Additional fields can be added here
    email = models.EmailField(unique=True)
    subscription_level = models.CharField(max_length=50, default='Free')


    def __str__(self):
        return self.username
