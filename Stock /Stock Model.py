from django.db import models
from django.contrib.auth.models import User

class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    market = models.CharField(max_length=50)
    price = models.FloatField(null=True, blank=True)
    market_cap = models.CharField(max_length=50, null=True, blank=True)
    pe_ratio = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.symbol

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stocks = models.ManyToManyField(Stock)

    def __str__(self):
        return f"{self.user.username}'s Portfolio"
