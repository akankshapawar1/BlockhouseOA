import requests
from datetime import datetime, timedelta
from .models import StockPrice
from django.http import JsonResponse
import os
API_KEY = os.getenv('API_KEY')

def fetch_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={API_KEY}'

    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json().get('Time Series (Daily)', {})
        
        if not data:
            return {'error': 'No data found from Alpha Vantage API.'}

        two_years_ago = datetime.now() - timedelta(days=2*365)

        for date, values in data.items():
            # Only store data from the past 2 years
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            if date_obj >= two_years_ago:
                StockPrice.objects.update_or_create(
                    symbol=symbol,
                    date=date,
                    defaults={
                        'open_price': values['1. open'],
                        'close_price': values['4. close'],
                        'high_price': values['2. high'],
                        'low_price': values['3. low'],
                        'volume': values['5. volume']
                    }
                )
        return {'status': 'Data fetched and stored successfully'}

    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

def fetch_stock_view(request, symbol):
    result = fetch_stock_data(symbol)
    if 'error' in result:
        return JsonResponse({'status': 'Error', 'message': result['error']}, status=400)
    return JsonResponse({'status': 'Data fetched successfully'})