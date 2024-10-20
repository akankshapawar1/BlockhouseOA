from django.db import models

# Create your models here.
class StockPrice(models.Model):
    symbol = models.CharField(max_length=10)
    date = models.DateField(null=True, blank=True)
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()

    # why this?
    def __str__(self):
        return f"{self.symbol}"