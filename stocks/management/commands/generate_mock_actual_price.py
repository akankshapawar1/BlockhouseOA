from random import uniform
from decimal import Decimal  # Import Decimal class
from stocks.models import StockPrediction
from django.core.management.base import BaseCommand

def generate_mock_actual_prices(symbol):
    # Fetch all predictions for the given symbol
    predictions = StockPrediction.objects.filter(symbol=symbol, actual_price__isnull=True)

    if not predictions.exists():
        print("No predictions found without actual prices.")
        return

    for prediction in predictions:
        # Generate a mock actual price by adding a small random change to the predicted price
        # For example, actual price can vary by +/- 5% of the predicted price
        random_change = Decimal(uniform(-0.05, 0.05))  # Convert the random change to Decimal
        actual_price = prediction.predicted_price * (1 + random_change)

        # Update the actual price
        prediction.actual_price = actual_price
        prediction.save()

    print(f"Mock actual prices generated for {symbol}.")

class Command(BaseCommand):
    help = 'Generate mock actual prices for predictions'

    def add_arguments(self, parser):
        # Allow passing a stock symbol via the command line
        parser.add_argument(
            '--symbol',
            type=str,
            default='AAPL',  # Default symbol is 'AAPL' if none is provided
            help='The stock symbol for which to generate mock actual prices'
        )

    def handle(self, *args, **options):
        symbol = options['symbol']
        generate_mock_actual_prices(symbol)
        self.stdout.write(self.style.SUCCESS(f'Mock actual prices generated for {symbol}'))