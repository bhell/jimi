from django.db import models
from jimi.price import fields

class TestModel(models.Model):
    """Simple model to test MoneyField"""
    ident = models.IntegerField(primary_key=True, unique=True)
    price = fields.MoneyField(blank=True)
