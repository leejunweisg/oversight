from django.contrib import admin
from .models import Stock

# Register your models here.
admin.site.register(Stock) # register the stock model so that it can be edited on admin page
