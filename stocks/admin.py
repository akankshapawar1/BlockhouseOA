from django.contrib import admin
from .models import StockPrice, StockPrediction

@admin.register(StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'date', 'open_price', 'close_price', 'high_price', 'low_price', 'volume']


@admin.register(StockPrediction)
class StockPredictionAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'date', 'predicted_price', 'actual_price']
