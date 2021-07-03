from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
  email = models.EmailField("email address", unique=True, blank=False, null=False)

class Twitch(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  access_token = models.CharField(max_length=64)
  refresh_token = models.CharField(max_length=64)
  user_name = models.CharField(max_length=64)

class Streamlabs(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  access_token = models.CharField(max_length=64)

class Youtube(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  access_token = models.CharField(max_length=64)
  refresh_token = models.CharField(max_length=64)
