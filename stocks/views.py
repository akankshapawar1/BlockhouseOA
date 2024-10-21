from django.shortcuts import render
import requests
from datetime import datetime, timedelta
from .predict import predict_stock_prices
from .backtesting import backtest_moving_average_strategy
from .models import StockPrediction, StockPrice
from django.http import JsonResponse
import os
from tenacity import retry, stop_after_attempt, wait_fixed
from django.http import JsonResponse, FileResponse
from .utils import generate_pdf_report, compute_metrics

API_KEY = os.getenv('API_KEY')

def home_view(request):
    return render(request, 'home.html')

@retry(stop=stop_after_attempt(2), wait=wait_fixed(3))
def fetch_stock_data(symbol):
    url = f'https://www.alphavantage.co/query'
    
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'outputsize': 'full',
        'apikey': API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  

        if "Note" in response.json():
            return {'error': 'API rate limit reached. Please try again later.'}

        data = response.json().get('Time Series (Daily)', {})

        if not data:
            return {'error': 'No data found from Alpha Vantage API.'}

        # Process and store data for the past 2 years
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

    except requests.exceptions.Timeout:
        return {'error': 'The request timed out. Please try again later.'}

    except requests.exceptions.RequestException as e:
        return {'error': f'An error occurred: {str(e)}'}

def fetch_stock_view(request, symbol):
    result = fetch_stock_data(symbol)
    if 'error' in result:
        return JsonResponse({'status': 'Error', 'message': result['error']}, status=400)
    return JsonResponse({'status': 'Data fetched successfully'})

def backtest_view(request):
    symbol = request.GET.get('symbol', 'AAPL')  # Default to AAPL
    initial_investment = float(request.GET.get('initial_investment', 10000))
    short_window = int(request.GET.get('short_window', 50))
    long_window = int(request.GET.get('long_window', 200))
    
    result = backtest_moving_average_strategy(symbol, initial_investment, short_window, long_window)
    
    if 'error' in result:
        return JsonResponse({'status': 'Error', 'message': result['error']}, status=400)
    
    return JsonResponse({'status': 'Success', 'data': result})

def predict_view(request):
    symbol = request.GET.get('symbol', 'AAPL')  
    days = 30

    result = predict_stock_prices(symbol, days)

    if isinstance(result, dict) and 'error' in result:
        return JsonResponse({'status': 'Error', 'message': result['error']}, status=400)

    return JsonResponse({'status': 'Success', 'data': result})

def report_view(request, symbol):
    report_format = request.GET.get('format', 'pdf')
    backtesting_results = backtest_moving_average_strategy(symbol, initial_investment=10000, short_window=50, long_window=200)
    predictions_exist = StockPrediction.objects.filter(symbol=symbol).exists()

    if report_format == 'pdf':
        buffer = generate_pdf_report(symbol)
        return FileResponse(buffer, as_attachment=True, filename=f"{symbol}_report.pdf")

    elif report_format == 'json':
        response_data = {
            'status': 'Success',
            'backtesting_results': {
                'total_return': backtesting_results['total_return'],
                'total_trades': backtesting_results['total_trades'],
                'max_drawdown': backtesting_results['max_drawdown']
            }
        }
        if predictions_exist:
            metrics = compute_metrics(symbol)
            response_data['prediction_results'] = metrics
        else:
            response_data['prediction_results'] = 'No predictions found for this symbol.'
        return JsonResponse(response_data)

    return JsonResponse({'status': 'Error', 'message': 'Invalid format specified'}, status=400)