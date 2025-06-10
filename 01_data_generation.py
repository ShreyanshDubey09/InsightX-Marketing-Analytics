import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Create directory structure first
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)
os.makedirs('data/results', exist_ok=True)
os.makedirs('sql', exist_ok=True)
os.makedirs('python', exist_ok=True)
os.makedirs('powerbi', exist_ok=True)
os.makedirs('documentation', exist_ok=True)

print("Project directories created successfully!")

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate 12,000 customers (to get 50K+ transactions)
print("Step 1: Generating customer data...")

customers_data = []
for i in range(1, 12001):
    # Create realistic customer profiles
    age = int(np.random.normal(40, 15))
    age = max(18, min(80, age))  # Ensure realistic age range
    
    gender = random.choice(['M', 'F'])
    registration_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))
    
    # Assign customer to a behavior type (affects spending patterns)
    behavior_type = random.choices(
        ['High_Value', 'Regular', 'Occasional', 'Bargain_Hunter'],
        weights=[0.15, 0.35, 0.35, 0.15]
    )[0]
    
    customers_data.append({
        'customer_id': i,
        'age': age,
        'gender': gender,
        'registration_date': registration_date,
        'behavior_type': behavior_type
    })

customers_df = pd.DataFrame(customers_data)
print(f"Generated {len(customers_df)} customers")

# Generate 55,000 transactions
print("Step 2: Generating transaction data...")

transactions_data = []
transaction_id = 1

for customer in customers_data:
    customer_id = customer['customer_id']
    behavior_type = customer['behavior_type']
    
    # Different transaction patterns based on behavior type
    if behavior_type == 'High_Value':
        num_transactions = random.randint(8, 25)
        avg_amount_base = 150
    elif behavior_type == 'Regular':
        num_transactions = random.randint(3, 12)
        avg_amount_base = 80
    elif behavior_type == 'Occasional':
        num_transactions = random.randint(1, 6)
        avg_amount_base = 60
    else:  # Bargain_Hunter
        num_transactions = random.randint(2, 8)
        avg_amount_base = 35
    
    for _ in range(num_transactions):
        # Generate transaction date (2024 data)
        transaction_date = datetime(2024, 1, 1) + timedelta(
            days=random.randint(0, 364)
        )
        
        # Generate amount with some variation
        amount = max(5, np.random.normal(avg_amount_base, avg_amount_base * 0.3))
        
        # Product categories with different probabilities
        category = random.choices(
            ['Electronics', 'Clothing', 'Home & Garden', 'Sports & Outdoors', 'Books & Media'],
            weights=[0.30, 0.25, 0.20, 0.15, 0.10]
        )[0]
        
        transactions_data.append({
            'transaction_id': transaction_id,
            'customer_id': customer_id,
            'transaction_date': transaction_date,
            'amount': round(amount, 2),
            'category': category
        })
        
        transaction_id += 1

transactions_df = pd.DataFrame(transactions_data)
print(f"Generated {len(transactions_df)} transactions")

# Save raw data
customers_df.to_csv('data/raw/customers.csv', index=False)
transactions_df.to_csv('data/raw/transactions.csv', index=False)
print("Raw data saved to CSV files successfully!")

# Display summary statistics
print("\n=== DATA GENERATION SUMMARY ===")
print(f"Total Customers: {len(customers_df):,}")
print(f"Total Transactions: {len(transactions_df):,}")
print(f"Date Range: {transactions_df['transaction_date'].min()} to {transactions_df['transaction_date'].max()}")
print(f"Total Revenue: ${transactions_df['amount'].sum():,.2f}")
print(f"Average Transaction: ${transactions_df['amount'].mean():.2f}")

print("\nCustomer Behavior Distribution:")
print(customers_df['behavior_type'].value_counts())

print("\nTransaction Categories:")
print(transactions_df['category'].value_counts())

print("\n✅ Step 1 completed successfully! Files saved in data/raw/ directory")

