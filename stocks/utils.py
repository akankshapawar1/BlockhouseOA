import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import base64
from decimal import Decimal
from .models import StockPrediction
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image
from django.conf import settings

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

def generate_comparison_plot(symbol):
    predictions = StockPrediction.objects.filter(symbol=symbol).order_by('date')

    dates = [prediction.date for prediction in predictions]
    predicted_prices = [prediction.predicted_price for prediction in predictions]
    actual_prices = [prediction.actual_price for prediction in predictions if prediction.actual_price is not None]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, predicted_prices, label='Predicted Prices', color='orange', linestyle='--')
    plt.plot(dates[:len(actual_prices)], actual_prices, label='Actual Prices', color='blue')
    plt.title(f'Predicted vs Actual Prices for {symbol}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()

    # Save the plot to a buffer to be included in the PDF
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return buffer  # Return the buffer with the plot

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image

def generate_pdf_report(symbol):
    # Compute metrics
    metrics = compute_metrics(symbol)
    
    # Generate plot
    plot_buffer = generate_comparison_plot(symbol)

    # Create a PDF file-like buffer
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Add title and metrics
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, f"Stock Prediction Report: {symbol}")

    c.setFont("Helvetica", 12)
    c.drawString(100, height - 80, f"Total Predictions: {metrics['total_predictions']}")
    c.drawString(100, height - 100, f"Mean Absolute Error: {metrics['mean_absolute_error']:.2f}")
    c.drawString(100, height - 120, f"Accuracy: {metrics['accuracy']:.2f}%")

    # Add the plot image
    plot_image = Image(plot_buffer)
    plot_image.drawHeight = 300  # Set plot height
    plot_image.drawWidth = 400   # Set plot width
    plot_image.wrapOn(c, width, height)
    plot_image.drawOn(c, 100, height - 450)

    # Finalize PDF
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer  # Return the buffer containing the PDF

