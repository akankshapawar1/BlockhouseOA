from django.utils import timezone
from django.test import TestCase
from .models import StockPrice
from .backtesting import backtest_moving_average_strategy

class BacktestTests(TestCase):
    def test_backtest_no_data(self):
        # Run backtest on a symbol with no data
        result = backtest_moving_average_strategy('TEST123', initial_investment=10000, short_window=50, long_window=200)
        self.assertEqual(result['error'], 'No data available for the given symbol.')

    def setUp(self):
        # Create some stock price data for TEST1234
        StockPrice.objects.create(
            symbol='TEST1234',
            date=timezone.now() - timezone.timedelta(days=2),
            open_price=140.00,  # Add open price
            close_price=150.00,  # Already exists
            high_price=155.00,   # Add high price
            low_price=135.00,    # Add low price
            volume=1000000       # Add volume
        )
        StockPrice.objects.create(
            symbol='TEST1234',
            date=timezone.now() - timezone.timedelta(days=1),
            open_price=145.00,
            close_price=155.00,
            high_price=160.00,
            low_price=140.00,
            volume=1200000
        )
        StockPrice.objects.create(
            symbol='TEST1234',
            date=timezone.now(),
            open_price=150.00,
            close_price=160.00,
            high_price=165.00,
            low_price=145.00,
            volume=1300000
        )

    def test_backtest_success(self):
        result = backtest_moving_average_strategy('TEST1234', initial_investment=10000, short_window=2, long_window=3)
        self.assertIn('total_return', result)
        self.assertIn('total_trades', result)
        self.assertIn('max_drawdown', result)
        self.assertGreaterEqual(result['total_return'], 0)
        self.assertGreaterEqual(result['total_trades'], 0)
        self.assertGreaterEqual(result['max_drawdown'], 0)

    def test_backtest_buy_sell_signal(self):
        StockPrice.objects.create(
            symbol='TEST1235',
            date=timezone.now() - timezone.timedelta(days=4),
            open_price=95.00,
            close_price=100.00,
            high_price=105.00,
            low_price=90.00,
            volume=1000000
        )
        StockPrice.objects.create(
            symbol='TEST1235',
            date=timezone.now() - timezone.timedelta(days=3),
            open_price=85.00,
            close_price=90.00,
            high_price=95.00,
            low_price=80.00,
            volume=1200000
        )
        StockPrice.objects.create(
            symbol='TEST1235',
            date=timezone.now() - timezone.timedelta(days=2),
            open_price=92.00,
            close_price=95.00,
            high_price=100.00,
            low_price=85.00,
            volume=1300000
        )
        StockPrice.objects.create(
            symbol='TEST1235',
            date=timezone.now() - timezone.timedelta(days=1),
            open_price=100.00,
            close_price=105.00,
            high_price=110.00,
            low_price=95.00,
            volume=1400000
        )
        StockPrice.objects.create(
            symbol='TEST1235',
            date=timezone.now(),
            open_price=105.00,
            close_price=110.00,
            high_price=115.00,
            low_price=100.00,
            volume=1500000
        )

        # Run backtest with small moving averages to ensure signals are triggered
        result = backtest_moving_average_strategy('TEST1235', initial_investment=10000, short_window=2, long_window=3)
        
        # Check that at least one trade has been executed
        self.assertGreater(result['total_trades'], 0)