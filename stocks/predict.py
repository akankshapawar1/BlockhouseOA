import os
import pickle
from datetime import timedelta
from decimal import Decimal
from django.conf import settings
import pandas as pd
from random import uniform
from .models import StockPrice, StockPrediction

def load_model():
    model_path = os.path.join(settings.BASE_DIR, 'stocks', 'linear_regression_model.pkl')
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

def predict_stock_prices(symbol, days=30):
    model = load_model()
    stock_data = StockPrice.objects.filter(symbol=symbol).order_by('date').values('date', 'close_price')

    if not stock_data.exists():
        return {'error': 'No data available for the given symbol.'}

    # Prepare data for prediction
    df = pd.DataFrame(stock_data)
    df['date'] = pd.to_datetime(df['date'])

    # Use the number of days as the input for prediction 
    last_day = df['date'].max()  
    X_future = [[i] for i in range(1, days + 1)]  

    # Predict future stock prices using the pre-trained model
    predicted_prices = model.predict(X_future)

    # Prepare the predictions for storing and returning
    predictions = []
    for i, predicted_price in enumerate(predicted_prices):
        future_date = last_day + timedelta(days=(i + 1))

        # Generate mock actual price (+/- 2% deviation from predicted price)
        random_change = uniform(-0.02, 0.02)  
        actual_price = Decimal(predicted_price) * (1 + Decimal(random_change))

        # Create and save the StockPrediction entry with both predicted and actual prices
        StockPrediction.objects.update_or_create(
            symbol=symbol,
            date=future_date,
            predicted_price=Decimal(predicted_price),
            actual_price=actual_price  
        )

        # Append the prediction to the list for returning
        predictions.append({
            'symbol': symbol,
            'date': future_date.strftime('%Y-%m-%d'),
            'predicted_price': float(predicted_price),
            'actual_price': float(actual_price)
        })

    return predictions  