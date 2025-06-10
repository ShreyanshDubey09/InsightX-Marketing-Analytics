import pandas as pd
import numpy as np
from datetime import datetime
import os

# Ensure directories exist
os.makedirs('data/processed', exist_ok=True)

print("Step 2: Loading data and calculating RFM metrics...")

# Load the data we created in Step 1
customers_df = pd.read_csv('data/raw/customers.csv')
transactions_df = pd.read_csv('data/raw/transactions.csv')

# Convert date column to datetime
transactions_df['transaction_date'] = pd.to_datetime(transactions_df['transaction_date'])
customers_df['registration_date'] = pd.to_datetime(customers_df['registration_date'])

print(f"Loaded {len(customers_df)} customers and {len(transactions_df)} transactions")

# Define analysis date (end of 2024)
analysis_date = datetime(2024, 12, 31)

print("Calculating RFM metrics...")

# Calculate RFM (Recency, Frequency, Monetary) metrics
rfm_data = transactions_df.groupby('customer_id').agg({
    'transaction_date': lambda x: (analysis_date - x.max()).days,  # Recency
    'transaction_id': 'count',  # Frequency
    'amount': ['sum', 'mean']  # Monetary
}).round(2)

# Flatten column names
rfm_data.columns = ['recency', 'frequency', 'monetary_total', 'monetary_avg']
rfm_data = rfm_data.reset_index()

# Merge with customer demographics
rfm_customers = rfm_data.merge(
    customers_df[['customer_id', 'age', 'gender', 'behavior_type']], 
    on='customer_id'
)

print(f"RFM analysis completed for {len(rfm_customers)} customers")

# Display RFM summary statistics
print("\n=== RFM ANALYSIS SUMMARY ===")
print("Recency (days since last purchase):")
print(f"  Mean: {rfm_customers['recency'].mean():.1f} days")
print(f"  Median: {rfm_customers['recency'].median():.1f} days")
print(f"  Range: {rfm_customers['recency'].min()}-{rfm_customers['recency'].max()} days")

print("\nFrequency (number of transactions):")
print(f"  Mean: {rfm_customers['frequency'].mean():.1f} transactions")
print(f"  Median: {rfm_customers['frequency'].median():.1f} transactions")
print(f"  Range: {rfm_customers['frequency'].min()}-{rfm_customers['frequency'].max()} transactions")

print("\nMonetary Total (total spent):")
print(f"  Mean: ${rfm_customers['monetary_total'].mean():.2f}")
print(f"  Median: ${rfm_customers['monetary_total'].median():.2f}")
print(f"  Range: ${rfm_customers['monetary_total'].min():.2f}-${rfm_customers['monetary_total'].max():.2f}")

# Save RFM data
rfm_customers.to_csv('data/processed/rfm_analysis.csv', index=False)
print(f"\n✅ RFM data saved to data/processed/rfm_analysis.csv")

# Preview the data
print("\n=== SAMPLE RFM DATA ===")
print(rfm_customers.head(10))

print("\n✅ Step 2 completed successfully!")
print("Next: Run Step 3 (K-means Clustering) or proceed to SQL database setup")
