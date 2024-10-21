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

### Deployment Access

The fully deployed application is accessible via a public URL. However, due to the limitations of the AWS free tier, I prefer not to share this URL publicly to avoid excessive usage and potential charges. This URL will be shared directly via email and in the file that I will be uploading on the Ashby page.

Thank you for your understanding!

### Important Note:

During the course of this project, I attempted to implement a CI/CD pipeline using GitHub Actions. However, I realized that integrating it fully with AWS CodeBuild would require additional configuration steps that I wasn’t able to complete due to time constraints. As a result, the CI/CD pipeline is not fully functional at the moment.

However, the application is fully deployed and functional on an AWS EC2 instance. You can access the application directly, and the setup on EC2 has been successfully integrated with AWS RDS for PostgreSQL. All features have been implemented, tested, and are working correctly in this environment.

If you’d like to run the project locally or check out the version prior to the CI/CD integration attempt, please follow the instructions below.

## Local Setup

### Step 1: Clone the repository

First, clone this repository:

```bash
git clone https://github.com/akankshapawar1/BlockhouseOA.git
cd BlockhouseOA
```
If you want to run the project locally as it was before CI/CD changes, please checkout the specific commit:
```bash
git checkout 41bc83e
```

Reason:
After this commit, the project configuration was changed to use GitHub Secrets for storing API keys and sensitive information, which are not available locally unless manually configured. Prior to this, environment variables were handled directly via the .env file, making local setup simpler for testing and development.

### Step 2: Set up a Python virtual environment

To create and activate a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

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
```

Generate a Django secret key with the following command:

```bash
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Replace your_django_secret_key, your_database_name, your_database_user, your_database_password, and your_alpha_vantage_api_key with your actual values.

### Step 6: Apply migrations

Once the database is set up and the .env file is configured, apply the database migrations:

```bash
python manage.py migrate
```
### Step 7: Seeding Data:
I have not seeded any sample data as part of this project. Therefore, once the migrations are complete, the database will be empty. You will need to either:
	•	Fetch live stock data through the application’s API to populate the database, or
	•	Manually insert data into the tables if required for testing or development.
You can use the fetch endpoint to gather data for specific stocks like this:
```bash
GET /fetch/<symbol>
```

### Step 8: Run the development server

Now you can run the development server:

```bash
python manage.py runserver
```

### Additional Commands

Run Tests

To run tests for the project:

```bash
python manage.py test
```

### Create a Superuser

To access the Django admin panel, you’ll need a superuser account. Create one using the following command:

```bash
python manage.py createsuperuser
```

Visit http://127.0.0.1:8000/admin/ and log in with your superuser credentials.

## How to Deploy to AWS

This section provides step-by-step instructions on how to deploy the Django application to AWS using Docker and Amazon RDS for PostgreSQL.

### Prerequisites

- **AWS Account**
- **AWS CLI**
- **SSH Key Pair**: Create an EC2 instance key pair for SSH access. Download the `.pem` file during the creation process.

### Step 1: Set Up the EC2 Instance

1. **Launch an EC2 Instance**

2. **Connect to the EC2 Instance**:
   ```bash
   ssh -i "your-key-file.pem" ec2-user@your-public-ip
   ```
### Step 2: Install Docker on EC2

Once connected to the EC2 instance, install Docker.

### Step 3: Set Up PostgreSQL RDS

	1.	Launch a PostgreSQL RDS Instance:
		•	Go to the RDS Dashboard in your AWS console.
		•	Click on “Create database.”
		•	Select PostgreSQL as the database engine.
		•	Configure database settings (DB instance identifier, master username, and password).
		•	Note down the database endpoint and connection details.
	2.	Configure Security Groups:
		•	Ensure that your RDS security group allows inbound connections from your EC2 instance.

### Step 4: Configure Environment Variables

	1.	Create a .env file in your project directory and add the following variables
 ```bash
SECRET_KEY=your_django_secret_key
POSTGRES_DB=your_database_name
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password
DB_HOST=your_rds_endpoint
DB_PORT=5432
```

### Step 5: Build and Run Docker Containers

	1.	Clone the Repository
 ```bash
git clone https://github.com/akankshapawar1/BlockhouseOA.git
cd BlockhouseOA
git checkout 41bc83e
```

	2.	Build the Docker Image and Run Containers:
 ```bash
docker-compose up --build
```

### Step 6: Run Migrations

After the containers are up and running, execute the following command to apply migrations:
```bash
docker-compose exec web python manage.py migrate
```

### Step 7: Access the Application

Open a web browser and navigate to http://your-ec2-public-ip:8000 to access your Django application.


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
