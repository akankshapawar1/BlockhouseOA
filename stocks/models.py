from django.db import models

# Create your models here.
class StockPrice(models.Model):
    symbol = models.CharField(max_length=10, db_index=True)
    date = models.DateField(null=True, blank=True, db_index=True)
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()
    class Meta:
        indexes = [
            models.Index(fields=['symbol', 'date']), 
        ]

    def __str__(self):
        return f"{self.symbol}"
    
class StockPrediction(models.Model):
    symbol = models.CharField(max_length=10)
    date = models.DateField()
    predicted_price = models.DecimalField(max_digits=10, decimal_places=2)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  

    def __str__(self):
        return f"Prediction for {self.symbol} on {self.date}: {self.predicted_price}"