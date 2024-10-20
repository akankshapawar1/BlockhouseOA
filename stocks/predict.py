import pickle
from datetime import timedelta
from decimal import Decimal
import pandas as pd
from .models import StockPrice, StockPrediction

# Load the pre-trained model
def load_model():
    with open('/Users/akanksha/Desktop/Stuff/Coding/BlockhouseOA/BlockhouseOA/linear_regression_model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

def predict_stock_prices(symbol, days=30):
    # Load the pre-trained model
    model = load_model()

    # Fetch historical data for the given symbol
    stock_data = StockPrice.objects.filter(symbol=symbol).order_by('date').values('date', 'close_price')

    if not stock_data.exists():
        return {'error': 'No data available for the given symbol.'}

    # Prepare data for prediction
    df = pd.DataFrame(stock_data)
    df['date'] = pd.to_datetime(df['date'])

    # Use the number of days as the input for prediction (simple linear regression on days)
    last_day = df['date'].max()  # Get the last date from the historical data
    X_future = [[i] for i in range(1, days + 1)]  # Future days

    # Predict future stock prices using the pre-trained model
    predicted_prices = model.predict(X_future)

    # Prepare the predictions for storing and returning
    predictions = []
    for i, predicted_price in enumerate(predicted_prices):
        future_date = last_day + timedelta(days=(i + 1))
        
        # Save the prediction to the StockPrediction model
        prediction = StockPrediction.objects.create(
            symbol=symbol,
            date=future_date,
            predicted_price=Decimal(predicted_price)  # Convert to Decimal for storing in the model
        )
        
        # Add the prediction to the list for the JSON response
        predictions.append({
            'symbol': symbol,
            'date': future_date.strftime('%Y-%m-%d'),
            'predicted_price': float(predicted_price)  # Convert Decimal or NumPy types to float
        })

    return predictions  # Return a list of dicts, which is JSON serializable

def compute_metrics(symbol):
    predictions = StockPrediction.objects.filter(symbol=symbol).order_by('date')

    total_predictions = predictions.count()
    total_error = Decimal(0)
    correct_predictions = 0

    for prediction in predictions:
        if prediction.actual_price is not None:
            error = abs(prediction.predicted_price - prediction.actual_price)
            total_error += error
            # Consider a prediction correct if it's within $5 of the actual price
            if error <= Decimal('5.00'):
                correct_predictions += 1

    # Calculate metrics
    mean_absolute_error = total_error / total_predictions if total_predictions > 0 else 0
    accuracy = (correct_predictions / total_predictions * 100) if total_predictions > 0 else 0

    return {
        'total_predictions': total_predictions,
        'mean_absolute_error': mean_absolute_error,
        'accuracy': accuracy
    }