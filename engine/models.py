from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Stock(models.Model):
    date = models.DateField(default=timezone.now)
    symbol = models.CharField(max_length=10) # assume max length 10
    shares = models.FloatField()
    price = models.FloatField()
    fees = models.FloatField()
    currency = models.CharField(max_length=5, default="USD")

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.symbol} ({self.shares} shares)"