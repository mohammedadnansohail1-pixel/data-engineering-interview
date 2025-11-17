"""Seed database with initial interview questions"""
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.question import Question

# Create tables
Base.metadata.create_all(bind=engine)


def seed_questions():
    """Seed initial questions into the database"""
    db = SessionLocal()

    try:
        # Check if questions already exist
        existing_count = db.query(Question).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} questions. Skipping seed.")
            return

        questions = [
            # SQL Questions
            {
                "title": "Calculate Running Total of Sales",
                "description": """Given a table 'sales' with columns (date, amount), write a SQL query to calculate the running total of sales ordered by date.

Table schema:
- sales (date DATE, amount DECIMAL)

Expected output columns: date, amount, running_total""",
                "category": "sql",
                "difficulty": "medium",
                "question_type": "coding",
                "starter_code": "SELECT \n  date,\n  amount,\n  -- Your code here\nFROM sales\nORDER BY date;",
                "test_cases": {
                    "sample_data": [
                        {"date": "2024-01-01", "amount": 100},
                        {"date": "2024-01-02", "amount": 150},
                        {"date": "2024-01-03", "amount": 200}
                    ],
                    "expected_result": [
                        {"date": "2024-01-01", "amount": 100, "running_total": 100},
                        {"date": "2024-01-02", "amount": 150, "running_total": 250},
                        {"date": "2024-01-03", "amount": 200, "running_total": 450}
                    ]
                },
                "companies": ["Amazon", "Google", "Meta"],
                "tags": ["window-functions", "sql", "aggregation"]
            },
            {
                "title": "Find Duplicate Records",
                "description": """Write a SQL query to find duplicate email addresses in a 'users' table.

Table schema:
- users (id INT, email VARCHAR, name VARCHAR)

Return: email addresses that appear more than once with their count.""",
                "category": "sql",
                "difficulty": "easy",
                "question_type": "coding",
                "starter_code": "SELECT \n  email,\n  COUNT(*) as count\nFROM users\n-- Your code here",
                "test_cases": {},
                "companies": ["Uber", "Airbnb"],
                "tags": ["sql", "grouping", "duplicates"]
            },
            {
                "title": "Second Highest Salary",
                "description": """Write a SQL query to find the second highest salary from an 'employees' table.

Table schema:
- employees (id INT, name VARCHAR, salary DECIMAL)

If there is no second highest salary, return NULL.""",
                "category": "sql",
                "difficulty": "medium",
                "question_type": "coding",
                "starter_code": "SELECT \n  -- Your code here\nFROM employees",
                "test_cases": {},
                "companies": ["Microsoft", "Oracle"],
                "tags": ["sql", "ranking", "subqueries"]
            },
            {
                "title": "Monthly Active Users",
                "description": """Calculate the monthly active users (MAU) from a 'user_activity' table.

Table schema:
- user_activity (user_id INT, activity_date DATE, activity_type VARCHAR)

Return: month, year, and count of distinct active users for each month.""",
                "category": "sql",
                "difficulty": "medium",
                "question_type": "coding",
                "starter_code": "SELECT \n  -- Your code here\nFROM user_activity\nGROUP BY -- Your code here",
                "test_cases": {},
                "companies": ["Meta", "LinkedIn"],
                "tags": ["sql", "date-functions", "metrics"]
            },
            {
                "title": "Join Tables with NULL Handling",
                "description": """Write a SQL query to join 'orders' and 'customers' tables, including customers who haven't placed any orders.

Table schemas:
- customers (customer_id INT, name VARCHAR)
- orders (order_id INT, customer_id INT, amount DECIMAL)

Return: customer_id, name, total_orders, total_amount (0 if no orders)""",
                "category": "sql",
                "difficulty": "easy",
                "question_type": "coding",
                "starter_code": "SELECT \n  -- Your code here\nFROM customers\n-- Your join here",
                "test_cases": {},
                "companies": ["Shopify", "Stripe"],
                "tags": ["sql", "joins", "null-handling"]
            },

            # Python/Spark Questions
            {
                "title": "Process CSV with Pandas",
                "description": """Write a Python function to read a CSV file, filter rows where 'age' > 25, and calculate the average salary by department.

Function signature:
def process_employee_data(csv_path: str) -> dict:
    # Returns dict with department as key and average salary as value
    pass

Expected CSV columns: name, age, department, salary""",
                "category": "python",
                "difficulty": "easy",
                "question_type": "coding",
                "starter_code": """import pandas as pd

def process_employee_data(csv_path: str) -> dict:
    # Your code here
    pass
""",
                "test_cases": [
                    {
                        "function": "process_employee_data",
                        "args": ["/tmp/test.csv"],
                        "expected": {"Engineering": 95000, "Sales": 75000}
                    }
                ],
                "companies": ["Netflix", "Spotify"],
                "tags": ["python", "pandas", "data-processing"]
            },
            {
                "title": "Deduplicate Records in PySpark",
                "description": """Write a PySpark function to deduplicate records based on 'user_id' and 'date', keeping the latest record by 'timestamp'.

Function signature:
def deduplicate_records(df: DataFrame) -> DataFrame:
    # Returns deduplicated DataFrame
    pass

Columns: user_id, date, timestamp, value""",
                "category": "python",
                "difficulty": "medium",
                "question_type": "coding",
                "starter_code": """from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window

def deduplicate_records(df: DataFrame) -> DataFrame:
    # Your code here
    pass
""",
                "test_cases": [],
                "companies": ["Databricks", "Uber"],
                "tags": ["pyspark", "deduplication", "window-functions"]
            },
            {
                "title": "Parse JSON Logs",
                "description": """Write a Python function to parse JSON log lines and extract error messages.

Function signature:
def extract_errors(log_file: str) -> list:
    # Returns list of error messages
    pass

Each log line is a JSON object with fields: timestamp, level, message""",
                "category": "python",
                "difficulty": "easy",
                "question_type": "coding",
                "starter_code": """import json

def extract_errors(log_file: str) -> list:
    # Your code here
    pass
""",
                "test_cases": [],
                "companies": ["Datadog", "Splunk"],
                "tags": ["python", "json", "parsing"]
            },
            {
                "title": "Aggregate Time Series Data",
                "description": """Write a function to aggregate time series data by hour and calculate mean, min, max values.

Function signature:
def aggregate_timeseries(data: list) -> list:
    # Input: list of dicts with 'timestamp' and 'value'
    # Output: list of dicts with 'hour', 'mean', 'min', 'max'
    pass""",
                "category": "python",
                "difficulty": "medium",
                "question_type": "coding",
                "starter_code": """from datetime import datetime
from collections import defaultdict

def aggregate_timeseries(data: list) -> list:
    # Your code here
    pass
""",
                "test_cases": [],
                "companies": ["InfluxDB", "TimescaleDB"],
                "tags": ["python", "time-series", "aggregation"]
            },
            {
                "title": "Implement Data Validation Pipeline",
                "description": """Create a data validation class that checks:
1. No NULL values in required fields
2. Email format is valid
3. Age is between 0 and 150

Class signature:
class DataValidator:
    def __init__(self, required_fields: list):
        pass

    def validate(self, record: dict) -> tuple:
        # Returns (is_valid: bool, errors: list)
        pass
""",
                "category": "python",
                "difficulty": "medium",
                "question_type": "coding",
                "starter_code": """import re

class DataValidator:
    def __init__(self, required_fields: list):
        # Your code here
        pass

    def validate(self, record: dict) -> tuple:
        # Your code here
        pass
""",
                "test_cases": [],
                "companies": ["Segment", "Fivetran"],
                "tags": ["python", "validation", "data-quality"]
            },

            # System Design Questions
            {
                "title": "Design a Data Lake Architecture",
                "description": """Design a data lake architecture for a company processing 10TB of data daily from various sources (APIs, databases, logs).

Requirements:
- Batch and streaming ingestion
- Data quality checks
- Cost optimization
- Query performance for analytics

Describe:
1. Architecture components
2. Technology choices
3. Data organization strategy
4. Scalability approach""",
                "category": "system_design",
                "difficulty": "hard",
                "question_type": "design",
                "starter_code": None,
                "test_cases": None,
                "companies": ["AWS", "Snowflake", "Databricks"],
                "tags": ["system-design", "data-lake", "architecture"]
            },
            {
                "title": "Design ETL Pipeline for E-commerce",
                "description": """Design an ETL pipeline to process e-commerce transactions in real-time and generate daily reports.

Requirements:
- Process 100K transactions/hour
- Real-time fraud detection
- Daily sales reports
- Customer analytics
- Handle late-arriving data

Discuss:
1. Pipeline architecture
2. Data flow
3. Error handling
4. Monitoring""",
                "category": "system_design",
                "difficulty": "hard",
                "question_type": "design",
                "starter_code": None,
                "test_cases": None,
                "companies": ["Shopify", "Amazon"],
                "tags": ["system-design", "etl", "real-time"]
            },
            {
                "title": "Design Data Warehouse Schema",
                "description": """Design a data warehouse schema for a SaaS company tracking user behavior, subscriptions, and revenue.

Requirements:
- Support complex analytics queries
- Handle time-series data efficiently
- Track slowly changing dimensions
- Optimize for query performance

Describe:
1. Schema design (fact and dimension tables)
2. Partitioning strategy
3. Indexing approach
4. Historical data handling""",
                "category": "system_design",
                "difficulty": "hard",
                "question_type": "design",
                "starter_code": None,
                "test_cases": None,
                "companies": ["Looker", "Tableau"],
                "tags": ["system-design", "data-warehouse", "schema"]
            },

            # Behavioral Questions
            {
                "title": "Describe a Complex Data Pipeline You Built",
                "description": """Tell me about the most complex data pipeline you've designed and implemented.

Use the STAR format:
- Situation: What was the context?
- Task: What was your responsibility?
- Action: What did you do?
- Result: What was the outcome?

Focus on:
- Technical challenges
- Design decisions
- Trade-offs
- Measurable impact""",
                "category": "behavioral",
                "difficulty": "medium",
                "question_type": "behavioral",
                "starter_code": None,
                "test_cases": None,
                "companies": ["All"],
                "tags": ["behavioral", "star", "experience"]
            },
            {
                "title": "Handling Data Quality Issues",
                "description": """Describe a time when you discovered significant data quality issues in a production system.

Address:
- How did you discover the issue?
- What was the impact?
- How did you resolve it?
- What processes did you implement to prevent future issues?

Use STAR format in your response.""",
                "category": "behavioral",
                "difficulty": "medium",
                "question_type": "behavioral",
                "starter_code": None,
                "test_cases": None,
                "companies": ["All"],
                "tags": ["behavioral", "data-quality", "problem-solving"]
            },
            {
                "title": "Conflict Resolution with Stakeholders",
                "description": """Tell me about a time when you disagreed with a stakeholder about data architecture or pipeline design.

Include:
- What was the disagreement about?
- How did you communicate your perspective?
- What was the resolution?
- What did you learn?

Use STAR format.""",
                "category": "behavioral",
                "difficulty": "medium",
                "question_type": "behavioral",
                "starter_code": None,
                "test_cases": None,
                "companies": ["All"],
                "tags": ["behavioral", "communication", "conflict"]
            },
        ]

        # Add questions to database
        for q_data in questions:
            question = Question(**q_data)
            db.add(question)

        db.commit()
        print(f"Successfully seeded {len(questions)} questions!")

    except Exception as e:
        print(f"Error seeding questions: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_questions()
