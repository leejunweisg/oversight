from django.contrib import admin
from .models import Profile

# Register your models here.
admin.site.register(Profile) # register the profile model so that it can be edited on admin page
