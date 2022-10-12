from django.contrib import admin
from .models import users, contact_form

# Register your models here.

admin.site.register(users)
admin.site.register(contact_form)
