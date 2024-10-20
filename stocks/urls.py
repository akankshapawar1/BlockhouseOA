from django.urls import path
from .views import fetch_stock_view

urlpatterns = [
    path('fetch/<str:symbol>/', fetch_stock_view, name='fetch_stock_data'),
]