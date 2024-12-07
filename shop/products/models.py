from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price_usd = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(decimal_places=1, max_digits=2)
    is_vip = models.BooleanField(default=False)

    def __str__(self):
        return self.name
