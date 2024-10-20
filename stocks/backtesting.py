import pandas as pd
from decimal import Decimal
from .models import StockPrice

def calculate_moving_averages(data, short_window=50, long_window=200):
    # Convert data to DataFrame
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Calculate moving averages
    df['50_MA'] = df['close_price'].rolling(window=short_window).mean()
    df['200_MA'] = df['close_price'].rolling(window=long_window).mean()
    
    return df

def backtest_moving_average_strategy(symbol, initial_investment, short_window=50, long_window=200):
    # Fetch historical stock prices for the symbol from the database
    stock_data = StockPrice.objects.filter(symbol=symbol).order_by('date').values('date', 'close_price')
    
    if not stock_data.exists():
        return {'error': 'No data available for the given symbol.'}
    
    # Convert the initial investment to Decimal for precision
    cash = Decimal(initial_investment)
    holdings = Decimal(0)  # Number of shares held
    total_trades = 0
    portfolio_value_history = []
    max_drawdown = Decimal(0)
    peak_value = Decimal(initial_investment)

    # Convert the stock data into a DataFrame and calculate the moving averages
    df = calculate_moving_averages(stock_data, short_window, long_window)

    # Buy and sell signals based on moving averages
    for date, row in df.iterrows():
        current_price = Decimal(row['close_price'])  # Ensure price is Decimal
        short_ma = row['50_MA']
        long_ma = row['200_MA']

        # Buy signal: when short MA crosses below long MA
        if short_ma < long_ma and holdings == Decimal(0):
            holdings = cash / current_price  # Buy shares with all available cash
            cash = Decimal(0)
            total_trades += 1

        # Sell signal: when short MA crosses above long MA
        elif short_ma > long_ma and holdings > Decimal(0):
            cash = holdings * current_price  # Sell all holdings
            holdings = Decimal(0)
            total_trades += 1

        # Calculate current portfolio value
        portfolio_value = cash + holdings * current_price
        portfolio_value_history.append(portfolio_value)

        # Track peak portfolio value to calculate drawdown
        peak_value = max(peak_value, portfolio_value)
        drawdown = (peak_value - portfolio_value) / peak_value
        max_drawdown = max(max_drawdown, drawdown)

    # Final portfolio value
    final_portfolio_value = cash + holdings * df.iloc[-1]['close_price']
    total_return = (final_portfolio_value - Decimal(initial_investment)) / Decimal(initial_investment) * 100

    # Return the backtesting results
    return {
        'initial_investment': initial_investment,
        'final_portfolio_value': final_portfolio_value,
        'total_return': total_return,
        'total_trades': total_trades,
        'max_drawdown': max_drawdown,
    }