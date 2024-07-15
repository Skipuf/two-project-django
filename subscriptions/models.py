from django.contrib.auth.models import User
from django.db import models

from posts.models import Category


# Create your models here.

class Subscriber(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
    )
