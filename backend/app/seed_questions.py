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

            # Additional SQL Questions
            {
                "title": "Top N Records per Group",
                "description": """Write a SQL query to find the top 3 highest-paid employees in each department.

Table schema:
- employees (employee_id INT, name VARCHAR, department_id INT, salary DECIMAL)

Expected output: employee_id, name, department_id, salary, rank_in_dept""",
                "category": "sql",
                "difficulty": "medium",
                "question_type": "coding",
                "starter_code": "SELECT \n  employee_id,\n  name,\n  department_id,\n  salary\n  -- Your code here\nFROM employees",
                "test_cases": {},
                "companies": ["Microsoft", "Amazon", "Google"],
                "tags": ["sql", "window-functions", "ranking", "partitioning"]
            },
            {
                "title": "Pivot Table with CASE Statement",
                "description": """Create a pivot table showing total sales by product category for each quarter.

Table schema:
- sales (sale_id INT, product_category VARCHAR, sale_date DATE, amount DECIMAL)

Expected output: product_category, Q1_sales, Q2_sales, Q3_sales, Q4_sales""",
                "category": "sql",
                "difficulty": "hard",
                "question_type": "coding",
                "starter_code": "SELECT \n  product_category,\n  -- Your code here\nFROM sales\nGROUP BY product_category",
                "test_cases": {},
                "companies": ["Tableau", "Looker"],
                "tags": ["sql", "pivot", "aggregation", "case-statement"]
            },
            {
                "title": "Find Gaps in Sequential Data",
                "description": """Find missing sequence numbers in a table of transactions.

Table schema:
- transactions (transaction_id INT, timestamp TIMESTAMP)

Write a query to find gaps in transaction_id sequence. Return the missing transaction IDs.""",
                "category": "sql",
                "difficulty": "medium",
                "question_type": "coding",
                "starter_code": "-- Find missing transaction IDs\nSELECT \n  -- Your code here\nFROM transactions",
                "test_cases": {},
                "companies": ["PayPal", "Stripe"],
                "tags": ["sql", "gaps-and-islands", "sequences"]
            },
            {
                "title": "Cumulative Sum with Conditions",
                "description": """Calculate cumulative sum of order values, but reset the sum when a refund occurs.

Table schema:
- orders (order_id INT, order_date DATE, amount DECIMAL, is_refund BOOLEAN)

Expected output: order_id, order_date, amount, cumulative_sum""",
                "category": "sql",
                "difficulty": "hard",
                "question_type": "coding",
                "starter_code": "SELECT \n  order_id,\n  order_date,\n  amount\n  -- Your code here\nFROM orders\nORDER BY order_date",
                "test_cases": {},
                "companies": ["Shopify", "Amazon"],
                "tags": ["sql", "window-functions", "conditional-logic"]
            },

            # Additional Python Questions
            {
                "title": "Implement Custom Hash Table",
                "description": """Implement a simple hash table that supports get, put, and remove operations.

Requirements:
- Handle hash collisions using chaining
- Support dynamic resizing when load factor > 0.75
- O(1) average case for get/put operations

Class signature:
class HashTable:
    def __init__(self, initial_size=16):
        pass

    def put(self, key, value):
        pass

    def get(self, key):
        pass

    def remove(self, key):
        pass""",
                "category": "python",
                "difficulty": "hard",
                "question_type": "coding",
                "starter_code": """class HashTable:
    def __init__(self, initial_size=16):
        # Your code here
        pass

    def put(self, key, value):
        # Your code here
        pass

    def get(self, key):
        # Your code here
        pass

    def remove(self, key):
        # Your code here
        pass
""",
                "test_cases": [],
                "companies": ["Google", "Amazon"],
                "tags": ["python", "data-structures", "hash-table"]
            },
            {
                "title": "Stream Processing with Windowing",
                "description": """Implement a sliding window to calculate average of last N values in a data stream.

Function signature:
class MovingAverage:
    def __init__(self, window_size: int):
        pass

    def add(self, value: float) -> float:
        # Add value and return current moving average
        pass

Example:
ma = MovingAverage(3)
ma.add(1.0)  # returns 1.0
ma.add(2.0)  # returns 1.5
ma.add(3.0)  # returns 2.0
ma.add(4.0)  # returns 3.0 (average of 2, 3, 4)""",
                "category": "python",
                "difficulty": "medium",
                "question_type": "coding",
                "starter_code": """from collections import deque

class MovingAverage:
    def __init__(self, window_size: int):
        # Your code here
        pass

    def add(self, value: float) -> float:
        # Your code here
        pass
""",
                "test_cases": [
                    {
                        "function": "MovingAverage",
                        "operations": ["add", "add", "add", "add"],
                        "values": [1.0, 2.0, 3.0, 4.0],
                        "expected": [1.0, 1.5, 2.0, 3.0]
                    }
                ],
                "companies": ["Kafka", "Flink", "Spark"],
                "tags": ["python", "streaming", "sliding-window"]
            },
            {
                "title": "Optimize DataFrame Operations",
                "description": """Given a slow pandas operation, optimize it for better performance.

Current code (slow):
```python
import pandas as pd

def process_large_dataset(df):
    result = []
    for idx, row in df.iterrows():
        if row['value'] > 100:
            result.append({
                'id': row['id'],
                'category': row['category'],
                'doubled': row['value'] * 2
            })
    return pd.DataFrame(result)
```

Rewrite this function to be 10x+ faster using vectorized operations.""",
                "category": "python",
                "difficulty": "medium",
                "question_type": "coding",
                "starter_code": """import pandas as pd

def process_large_dataset(df):
    # Optimize this function
    # Original slow code uses iterrows()
    # Your optimized code here
    pass
""",
                "test_cases": [],
                "companies": ["Pandas", "NumPy"],
                "tags": ["python", "pandas", "optimization", "vectorization"]
            },
            {
                "title": "Implement Rate Limiter",
                "description": """Implement a rate limiter that allows N requests per time window.

Use the token bucket algorithm:
- Bucket starts with N tokens
- Each request consumes 1 token
- Tokens refill at rate R per second
- Return True if request allowed, False otherwise

Class signature:
class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        pass

    def allow_request(self) -> bool:
        pass""",
                "category": "python",
                "difficulty": "hard",
                "question_type": "coding",
                "starter_code": """import time

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        # Your code here
        pass

    def allow_request(self) -> bool:
        # Your code here
        pass
""",
                "test_cases": [],
                "companies": ["Redis", "AWS", "Cloudflare"],
                "tags": ["python", "rate-limiting", "algorithms"]
            },

            # Additional System Design Questions
            {
                "title": "Design a Real-time Analytics Dashboard",
                "description": """Design a system to power a real-time analytics dashboard showing user activity metrics.

Requirements:
- Ingest 50K events/second
- Display metrics with <5 second latency
- Support drill-down queries
- Handle spike traffic (3x normal)
- Store 90 days of raw data

Discuss:
1. Event ingestion architecture
2. Storage strategy (hot/warm/cold)
3. Query optimization techniques
4. Caching layer design
5. Scalability approach""",
                "category": "system_design",
                "difficulty": "hard",
                "question_type": "design",
                "starter_code": None,
                "test_cases": None,
                "companies": ["Datadog", "New Relic", "Splunk"],
                "tags": ["system-design", "real-time", "analytics", "streaming"]
            },
            {
                "title": "Design a Data Quality Monitoring System",
                "description": """Design a system to monitor data quality across hundreds of data pipelines.

Requirements:
- Detect schema changes automatically
- Identify data anomalies (nulls, outliers, duplicates)
- Alert on quality degradation
- Track data lineage
- Generate quality reports

Describe:
1. Architecture components
2. Quality checks to implement
3. Alerting strategy
4. Lineage tracking approach
5. Scalability considerations""",
                "category": "system_design",
                "difficulty": "hard",
                "question_type": "design",
                "starter_code": None,
                "test_cases": None,
                "companies": ["Great Expectations", "Monte Carlo", "Datafold"],
                "tags": ["system-design", "data-quality", "monitoring"]
            },

            # Additional Behavioral Questions
            {
                "title": "Handling Production Incidents",
                "description": """Tell me about a time when you had to troubleshoot and fix a critical production issue with a data pipeline.

Address using STAR format:
- Situation: What broke and what was the impact?
- Task: What was your role in fixing it?
- Action: How did you diagnose and resolve the issue?
- Result: What was the outcome and what did you learn?

Include:
- Debugging approach
- Communication with stakeholders
- Post-mortem actions""",
                "category": "behavioral",
                "difficulty": "medium",
                "question_type": "behavioral",
                "starter_code": None,
                "test_cases": None,
                "companies": ["All"],
                "tags": ["behavioral", "incident-response", "debugging"]
            },
            {
                "title": "Technical Leadership Experience",
                "description": """Describe a time when you led a technical initiative or mentored junior engineers.

Use STAR format and address:
- Situation: What was the project or mentorship situation?
- Task: What were you responsible for?
- Action: How did you lead or mentor?
- Result: What was the impact on the team/individual?

Focus on:
- Leadership style
- Teaching approach
- Challenges faced
- Outcomes achieved""",
                "category": "behavioral",
                "difficulty": "medium",
                "question_type": "behavioral",
                "starter_code": None,
                "test_cases": None,
                "companies": ["All"],
                "tags": ["behavioral", "leadership", "mentorship"]
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
