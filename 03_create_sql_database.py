import sqlite3
import pandas as pd
import os

print("Step 3: Creating SQL Database...")

# Create sql directory
os.makedirs('sql', exist_ok=True)

# Connect to SQLite database (creates if doesn't exist)
conn = sqlite3.connect('data/marketing_analysis.db')
cursor = conn.cursor()

print("Connected to SQLite database")

# Create customers table
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    age INTEGER,
    gender TEXT,
    registration_date DATE,
    behavior_type TEXT
)
''')

# Create transactions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    transaction_date DATE,
    amount REAL,
    category TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
''')

# Create RFM analysis table
cursor.execute('''
CREATE TABLE IF NOT EXISTS rfm_analysis (
    customer_id INTEGER PRIMARY KEY,
    recency INTEGER,
    frequency INTEGER,
    monetary_total REAL,
    monetary_avg REAL,
    age INTEGER,
    gender TEXT,
    behavior_type TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
''')

print("Database tables created successfully")

# Load and insert data
print("Loading data into database...")

# Load customers data
customers_df = pd.read_csv('data/raw/customers.csv')
customers_df.to_sql('customers', conn, if_exists='replace', index=False)
print(f"Inserted {len(customers_df)} customers")

# Load transactions data
transactions_df = pd.read_csv('data/raw/transactions.csv')
transactions_df.to_sql('transactions', conn, if_exists='replace', index=False)
print(f"Inserted {len(transactions_df)} transactions")

# Load RFM data (if it exists)
try:
    rfm_df = pd.read_csv('data/processed/rfm_analysis.csv')
    rfm_df.to_sql('rfm_analysis', conn, if_exists='replace', index=False)
    print(f"Inserted {len(rfm_df)} RFM records")
except FileNotFoundError:
    print("RFM analysis file not found. Run Step 2 first!")

# Test queries
print("\n=== TESTING DATABASE ===")

# Test query 1: Customer count by behavior type
print("Customer count by behavior type:")
result = cursor.execute('''
    SELECT behavior_type, COUNT(*) as customer_count
    FROM customers
    GROUP BY behavior_type
    ORDER BY customer_count DESC
''').fetchall()

for row in result:
    print(f"  {row[0]}: {row[1]}")

# Test query 2: Total revenue by category
print("\nTotal revenue by category:")
result = cursor.execute('''
    SELECT category, 
           COUNT(*) as transaction_count,
           ROUND(SUM(amount), 2) as total_revenue,
           ROUND(AVG(amount), 2) as avg_transaction
    FROM transactions
    GROUP BY category
    ORDER BY total_revenue DESC
''').fetchall()

for row in result:
    print(f"  {row[0]}: {row[1]} transactions, ${row[2]} revenue, ${row[3]} avg")

# Save SQL queries for future use
sql_queries = '''
-- Customer segmentation summary
SELECT 
    behavior_type,
    COUNT(*) as customer_count,
    AVG(age) as avg_age,
    COUNT(CASE WHEN gender = 'M' THEN 1 END) as male_count,
    COUNT(CASE WHEN gender = 'F' THEN 1 END) as female_count
FROM customers 
GROUP BY behavior_type
ORDER BY customer_count DESC;

-- Monthly transaction trends
SELECT 
    strftime('%Y-%m', transaction_date) as month,
    COUNT(*) as transaction_count,
    ROUND(SUM(amount), 2) as total_revenue,
    ROUND(AVG(amount), 2) as avg_transaction_amount
FROM transactions
GROUP BY strftime('%Y-%m', transaction_date)
ORDER BY month;

-- Top customers by total spending
SELECT 
    c.customer_id,
    c.age,
    c.gender,
    c.behavior_type,
    COUNT(t.transaction_id) as transaction_count,
    ROUND(SUM(t.amount), 2) as total_spent,
    ROUND(AVG(t.amount), 2) as avg_transaction
FROM customers c
JOIN transactions t ON c.customer_id = t.customer_id
GROUP BY c.customer_id, c.age, c.gender, c.behavior_type
ORDER BY total_spent DESC
LIMIT 20;

-- RFM analysis with customer info
SELECT 
    r.customer_id,
    r.recency,
    r.frequency,
    r.monetary_total,
    r.monetary_avg,
    c.behavior_type,
    c.age,
    c.gender
FROM rfm_analysis r
JOIN customers c ON r.customer_id = c.customer_id
ORDER BY r.monetary_total DESC;
'''

# Save queries to file
with open('sql/analysis_queries.sql', 'w') as f:
    f.write(sql_queries)

conn.close()
print(f"\n✅ Database created successfully: data/marketing_analysis.db")
print("✅ SQL queries saved to: sql/analysis_queries.sql")
print("\n✅ Step 3 completed successfully!")
