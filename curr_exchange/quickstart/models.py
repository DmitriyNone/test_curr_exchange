from django.db import models


class Currencies(models.Model):
    timestamp = models.IntegerField()
    usd = models.DecimalField(max_digits=12, decimal_places=6)
    eur = models.DecimalField(max_digits=12, decimal_places=6)
    czk = models.DecimalField(max_digits=12, decimal_places=6)
    pln = models.DecimalField(max_digits=12, decimal_places=6)
