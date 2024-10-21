# BlockhouseOA - Backend Engineer Trial Task

This Django project fetches financial data, performs backtesting on stock prices, integrates machine learning predictions, and generates performance reports for backtesting or/and predictions in JSON and PDF format.

## Features
- Fetch stock price data from the Alpha Vantage API.
- Implement backtesting strategies.
- Predict future stock prices using a pre-trained machine learning model.
- Generate PDF and JSON reports.
  
---

## Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.9 or higher
- PostgreSQL 
- Git
- [Alpha Vantage API key](https://www.alphavantage.co/support/#api-key)

---

## Local Setup

### Step 1: Clone the repository

First, clone this repository:

```bash
git clone https://github.com/akankshapawar1/BlockhouseOA.git
cd BlockhouseOA

### Step 2: Set up a Python virtual environment

To create and activate a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

### Step 3: Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt

### Step 4: Set up PostgreSQL

Ensure PostgreSQL is installed and running on your local machine. You’ll need to create a database and user for this project.

### Step 5: Set up environment variables

Create a .env file in the root directory of the project and add the following environment variables:

```bash
SECRET_KEY=your_django_secret_key
POSTGRES_DB=your_database_name
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
API_KEY=your_alpha_vantage_api_key

Generate a Django secret key with the following command:

```bash
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())

Replace your_django_secret_key, your_database_name, your_database_user, your_database_password, and your_alpha_vantage_api_key with your actual values.

### Step 6: Apply migrations

Once the database is set up and the .env file is configured, apply the database migrations:

```bash
python manage.py migrate

Step 8: Run the development server

Now you can run the development server:

```bash
python manage.py runserver


### Additional Commands

Run Tests

To run tests for the project:

```bash
python manage.py test

### Create a Superuser

To access the Django admin panel, you’ll need a superuser account. Create one using the following command:

```bash
python manage.py createsuperuser

Visit http://127.0.0.1:8000/admin/ and log in with your superuser credentials.


### API Documentation

	1.	Fetch Stock Data: Use the /fetch/ endpoint with the stock symbol as a parameter to fetch stock price data.
	•	GET /fetch/?symbol=AAPL
	2.	Backtesting: Use the /backtest/ endpoint to perform a backtest with initial investment and moving averages.
	•	GET /backtest/?symbol=AAPL&initial_investment=10000&short_window=50&long_window=200
	3.	Predict Stock Prices: Use the /predict/ endpoint to get stock price predictions for the next 30 days.
	•	GET /predict/?symbol=AAPL
	4.	Generate Report: Use the /report/ endpoint to generate a PDF or JSON report.
	•	GET /report/?symbol=AAPL&format=pdf
	•	GET /report/?symbol=AAPL&format=json
