# stocks/management/commands/train_model.py

from django.core.management.base import BaseCommand
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
from stocks.models import StockPrice  # Import your Django models

class Command(BaseCommand):
    help = 'Train the Linear Regression model based on stock prices'

    def handle(self, *args, **kwargs):
        # Fetch historical stock data for training
        stock_data = StockPrice.objects.filter(symbol='AAPL').order_by('date').values('date', 'close_price')

        if not stock_data.exists():
            self.stdout.write(self.style.ERROR('No data available for the given symbol.'))
            return

        # Prepare data for training
        df = pd.DataFrame(stock_data)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        df['day'] = range(1, len(df) + 1)  # Day numbers
        X = df[['day']].values  # Feature (days)
        y = df['close_price'].values  # Target (prices)

        # Train the model
        model = LinearRegression()
        model.fit(X, y)

        # Save the trained model
        with open('linear_regression_model.pkl', 'wb') as file:
            pickle.dump(model, file)

        self.stdout.write(self.style.SUCCESS('Model trained and saved successfully.'))