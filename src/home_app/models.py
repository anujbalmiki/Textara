from datetime import date
from django.db import models

# Create your models here.


class user_activity(models.Model):
    text = models.TextField()
    user_name = models.TextField(max_length=254)
    date = models.DateTimeField()
