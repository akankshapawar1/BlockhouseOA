from django.contrib import admin
from .models import StockPrice

@admin.register(StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'open_price', 'close_price', 'high_price', 'low_price', 'volume']