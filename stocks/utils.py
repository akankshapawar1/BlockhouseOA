import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
from decimal import Decimal
from .models import StockPrediction
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image
import matplotlib.pyplot as plt
from .backtesting import backtest_moving_average_strategy
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
import io
from reportlab.platypus import Spacer


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
    # Create a PDF file-like buffer
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, title=f"{symbol} Stock Prediction Report")

    # Elements to add to the document
    elements = []

    # Add title
    styles = getSampleStyleSheet()
    title = Paragraph(f"Stock Prediction Report: {symbol}", styles['Title'])
    elements.append(title)

    # Subheading for Backtesting Results
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Backtesting Results", styles['Heading2']))

    # Compute backtesting results
    backtest_result = backtest_moving_average_strategy(symbol, 10000)  # Example call to backtest
    elements.append(Paragraph(f"Total Return: {backtest_result['total_return']:.2f}%", styles['Normal']))
    elements.append(Paragraph(f"Total Trades: {backtest_result['total_trades']}", styles['Normal']))
    elements.append(Paragraph(f"Max Drawdown: {backtest_result['max_drawdown']:.2f}", styles['Normal']))

    # Add spacer between sections
    elements.append(Spacer(1, 24))

    # Subheading for ML Predictions
    elements.append(Paragraph("ML Predictions", styles['Heading2']))

    # Fetch predictions
    predictions = StockPrediction.objects.filter(symbol=symbol).order_by('date')

    # Handle case when predictions are not available
    if not predictions.exists():
        elements.append(Paragraph("Predictions not available yet for this stock symbol.", styles['Normal']))

        # Build the document and return it (since no predictions exist)
        doc.build(elements)
        buffer.seek(0)
        return buffer

    # If predictions exist, compute ML performance metrics
    metrics = compute_metrics(symbol)

    # Add metrics to the report
    elements.append(Paragraph(f"Total Predictions: {metrics['total_predictions']}", styles['Normal']))
    elements.append(Paragraph(f"Mean Absolute Error: {metrics['mean_absolute_error']:.2f}", styles['Normal']))
    elements.append(Paragraph(f"Accuracy: {metrics['accuracy']:.2f}%", styles['Normal']))

    # Add a spacer
    elements.append(Spacer(1, 24))

    # Add ML predictions plot
    plot_buffer = generate_comparison_plot(symbol)
    plot_image = Image(plot_buffer)
    plot_image.drawHeight = 300  # Set plot height
    plot_image.drawWidth = 400   # Set plot width
    elements.append(plot_image)

    # Add spacer between plot and table
    elements.append(Spacer(1, 24))

    # Table with column headers for predicted prices only
    table_data = [["Date", "Predicted Price"]]  # Column headers
    for prediction in predictions:
        table_data.append([
            prediction.date.strftime('%Y-%m-%d'),
            f"${prediction.predicted_price:.2f}"
        ])

    # Create and style the table
    table = Table(table_data, colWidths=[2 * inch, 2 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Add the table to the document
    elements.append(table)

    # Build the document
    doc.build(elements)

    buffer.seek(0)
    return buffer