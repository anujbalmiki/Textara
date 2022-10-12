from pyexpat import model
from unicodedata import name
from django.db import models

# Create your models here.


class users(models.Model):
    name = models.TextField(max_length=191)
    email = models.EmailField(max_length=254)
    password = models.TextField(max_length=191)
    user_name = models.TextField(max_length=191)


# contact form model
class contact_form(models.Model):
    name = models.TextField(max_length=191)
    email = models.EmailField(max_length=254)
    subject = models.TextField(max_length=254)
    message = models.TextField(max_length=500)
