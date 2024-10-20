from django.urls import path
from .views import backtest_view, fetch_stock_view, predict_view

urlpatterns = [
    path('fetch/<str:symbol>/', fetch_stock_view, name='fetch_stock_data'),
    path('backtest/', backtest_view, name='backtest'),
    path('predict/', predict_view, name='predict'),
]