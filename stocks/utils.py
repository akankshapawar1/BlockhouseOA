import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
from decimal import Decimal
from .models import StockPrediction
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image
import matplotlib.pyplot as plt
import io
from .backtesting import backtest_moving_average_strategy

# Function to compute key metrics
def compute_metrics(symbol):
    predictions = StockPrediction.objects.filter(symbol=symbol).order_by('date')
    total_predictions = predictions.count()
    total_error = Decimal(0)
    correct_predictions = 0

    for prediction in predictions:
        if prediction.actual_price is not None:
            error = abs(prediction.predicted_price - prediction.actual_price)
            total_error += error
            # Consider a prediction correct if it's within $1.5 of the actual price
            if error <= Decimal('1.5'):
                correct_predictions += 1

    # Calculate metrics
    mean_absolute_error = total_error / total_predictions if total_predictions > 0 else 0
    accuracy = (correct_predictions / total_predictions * 100) if total_predictions > 0 else 0

    return {
        'total_predictions': total_predictions,
        'mean_absolute_error': mean_absolute_error,
        'accuracy': accuracy
    }

def generate_comparison_plot(symbol):
    predictions = StockPrediction.objects.filter(symbol=symbol).order_by('date')

    # Separate dates, predicted prices, and actual prices
    dates = [prediction.date for prediction in predictions]
    predicted_prices = [prediction.predicted_price for prediction in predictions]
    actual_prices = [prediction.actual_price for prediction in predictions if prediction.actual_price is not None]
    
    # Initialize the plot
    plt.figure(figsize=(10, 6))

    # Plot predicted prices (dashed line)
    plt.plot(dates, predicted_prices, label='Predicted Prices', color='orange', linestyle='--', marker='o')
    
    # Plot actual prices (solid line with markers)
    plt.plot(dates[:len(actual_prices)], actual_prices, label='Actual Prices', color='blue', linestyle='-', marker='s')

    # Add title and labels with larger font sizes
    plt.title(f'Predicted vs Actual Prices for {symbol}', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price', fontsize=12)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Add gridlines for better readability
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Add legend with larger font size
    plt.legend(fontsize=12)

    # Use tight layout to avoid overlap
    plt.tight_layout()

    # Save the plot to a buffer to be included in the PDF
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return buffer  # Return the buffer with the plot

def generate_pdf_report(symbol):
    # Check if any predictions exist for the symbol
    predictions_exist = StockPrediction.objects.filter(symbol=symbol).exists()

    # Compute backtesting metrics (this will always run, even if there are no predictions)
    backtesting_results = backtest_moving_average_strategy(symbol, initial_investment=10000, short_window=50, long_window=200)

    # Create a PDF file-like buffer
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    # Set the PDF metadata
    c.setTitle(f"{symbol} Stock Prediction Report")
    width, height = letter

    # Add title and backtesting results
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, f"Stock Report: {symbol}")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, height - 100, "Backtesting Results")

    c.setFont("Helvetica", 12)
    c.drawString(100, height - 120, f"Total Return: {backtesting_results['total_return']:.2f}%")
    c.drawString(100, height - 140, f"Total Trades: {backtesting_results['total_trades']}")
    c.drawString(100, height - 160, f"Max Drawdown: {backtesting_results['max_drawdown']:.2f}%")

    # Check if predictions exist, and include prediction metrics and plot if they do
    if predictions_exist:
        # Compute prediction metrics
        metrics = compute_metrics(symbol)

        # Add prediction metrics
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, height - 200, "Prediction Results")

        c.setFont("Helvetica", 12)
        c.drawString(100, height - 220, f"Total Predictions: {metrics['total_predictions']}")
        c.drawString(100, height - 240, f"Mean Absolute Error: {metrics['mean_absolute_error']:.2f}")
        c.drawString(100, height - 260, f"Accuracy: {metrics['accuracy']:.2f}%")

        # Generate and add the plot
        plot_buffer = generate_comparison_plot(symbol)
        plot_image = Image(plot_buffer)
        plot_image.drawHeight = 300  # Set plot height
        plot_image.drawWidth = 400   # Set plot width
        plot_image.wrapOn(c, width, height)
        plot_image.drawOn(c, 100, height - 550)

    else:
        # If no predictions exist, provide a message indicating that predictions are not available
        c.setFont("Helvetica", 12)
        c.drawString(100, height - 220, "No predictions found for this symbol.")
        c.drawString(100, height - 240, "Please run the prediction step to include prediction data.")

    # Finalize PDF
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer 