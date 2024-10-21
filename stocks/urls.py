from django.urls import path
from .views import backtest_view, fetch_stock_view, home_view, predict_view, report_view

urlpatterns = [
    path('', home_view, name='home'),
    path('fetch/<str:symbol>/', fetch_stock_view, name='fetch_stock_data'),
    path('backtest/', backtest_view, name='backtest'),
    path('predict/', predict_view, name='predict'),
    path('report/<str:symbol>/', report_view, name='report_view'),
]