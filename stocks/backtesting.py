import pandas as pd
from decimal import Decimal
from .models import StockPrice

def calculate_moving_averages(data, short_window=50, long_window=200):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    short_ma_col = f'{short_window}_MA'
    long_ma_col = f'{long_window}_MA'

    df[short_ma_col] = df['close_price'].rolling(window=short_window).mean()
    df[long_ma_col] = df['close_price'].rolling(window=long_window).mean()
    
    return df, short_ma_col, long_ma_col

def backtest_moving_average_strategy(symbol, initial_investment, short_window=50, long_window=200):
    # Fetch historical stock prices for the symbol from the database
    stock_data = StockPrice.objects.filter(symbol=symbol).order_by('date').values('date', 'close_price')
    
    if not stock_data.exists():
        return {'error': 'No data available for the given symbol.'}
    
    cash = Decimal(initial_investment)
    holdings = Decimal(0)  
    total_trades = 0
    portfolio_value_history = []
    max_drawdown = Decimal(0)
    peak_value = Decimal(initial_investment)

    df, short_ma_col, long_ma_col = calculate_moving_averages(stock_data, short_window, long_window)

    # Buy and sell signals based on moving averages
    for date, row in df.iterrows():
        current_price = Decimal(row['close_price'])  
        short_ma = row[short_ma_col]
        long_ma = row[long_ma_col]

        # Buy signal: when short MA crosses below long MA
        if short_ma < long_ma and holdings == Decimal(0):
            holdings = cash / current_price 
            cash = Decimal(0)
            total_trades += 1

        # Sell signal: when short MA crosses above long MA
        elif short_ma > long_ma and holdings > Decimal(0):
            cash = holdings * current_price  
            holdings = Decimal(0)
            total_trades += 1

        portfolio_value = cash + holdings * current_price
        portfolio_value_history.append(portfolio_value)

        # Track peak portfolio value to calculate drawdown
        peak_value = max(peak_value, portfolio_value)
        drawdown = (peak_value - portfolio_value) / peak_value
        max_drawdown = max(max_drawdown, drawdown)

    final_portfolio_value = cash + holdings * df.iloc[-1]['close_price']
    total_return = (final_portfolio_value - Decimal(initial_investment)) / Decimal(initial_investment) * 100

    return {
        'total_return': total_return,
        'total_trades': total_trades,
        'max_drawdown': max_drawdown,
    }