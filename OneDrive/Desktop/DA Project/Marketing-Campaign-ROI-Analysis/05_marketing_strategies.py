import pandas as pd
import numpy as np
import json
import os

print("Step 5: Developing targeted marketing strategies...")

# Load segmented customer data
customer_segments = pd.read_csv('data/processed/customer_segments.csv')
print(f"Loaded {len(customer_segments)} segmented customers")

# Load segment definitions
with open('data/processed/segment_definitions.json', 'r') as f:
    segment_definitions = json.load(f)

# Define detailed campaign strategies for each segment
campaign_strategies = {
    0: {  # Champions
        'email_subject_generic': 'Check Out Our Latest Offers',
        'email_subject_targeted': 'Exclusive VIP Access - New Premium Collection',
        'discount_percent': 15,
        'campaign_type': 'Premium Product Launch',
        'expected_ctr_base': 0.12,
        'send_frequency': 'Weekly',
        'channel_priority': 'Email + SMS + Push'
    },
    1: {  # Loyal Customers
        'email_subject_generic': 'Check Out Our Latest Offers', 
        'email_subject_targeted': 'Your Favorites Are Back in Stock!',
        'discount_percent': 10,
        'campaign_type': 'Product Restock Alert',
        'expected_ctr_base': 0.09,
        'send_frequency': 'Bi-weekly',
        'channel_priority': 'Email + Push'
    },
    2: {  # At Risk
        'email_subject_generic': 'Check Out Our Latest Offers',
        'email_subject_targeted': 'We Miss You! 20% Off Everything',
        'discount_percent': 20,
        'campaign_type': 'Win-Back Campaign',
        'expected_ctr_base': 0.06,
        'send_frequency': 'Monthly',
        'channel_priority': 'Email + Direct Mail'
    },
    3: {  # Potential Loyalists
        'email_subject_generic': 'Check Out Our Latest Offers',
        'email_subject_targeted': 'Complete Your Style - Special Member Pricing',
        'discount_percent': 12,
        'campaign_type': 'Cross-Sell Campaign',
        'expected_ctr_base': 0.08,
        'send_frequency': 'Bi-weekly',
        'channel_priority': 'Email + Social Media'
    }
}

# Create detailed campaign assignments
print("Creating campaign assignments...")

campaign_data = []
for _, customer in customer_segments.iterrows():
    cluster = int(customer['cluster'])  # Ensure integer key
    strategy = campaign_strategies[cluster]
    
    campaign_data.append({
        'customer_id': customer['customer_id'],
        'cluster': cluster,
        'segment_name': customer['segment_name'],
        'age': customer['age'],
        'gender': customer['gender'],
        'recency': customer['recency'],
        'frequency': customer['frequency'],
        'monetary_total': customer['monetary_total'],
        'email_subject_generic': strategy['email_subject_generic'],
        'email_subject_targeted': strategy['email_subject_targeted'],
        'discount_percent': strategy['discount_percent'],
        'campaign_type': strategy['campaign_type'],
        'expected_ctr_base': strategy['expected_ctr_base'],
        'send_frequency': strategy['send_frequency'],
        'channel_priority': strategy['channel_priority']
    })

campaign_df = pd.DataFrame(campaign_data)
print(f"Campaign strategies assigned to {len(campaign_df)} customers")

# Display campaign summary
print("\n=== CAMPAIGN STRATEGY SUMMARY ===")
campaign_summary = campaign_df.groupby(['segment_name', 'campaign_type']).agg({
    'customer_id': 'count',
    'discount_percent': 'first',
    'expected_ctr_base': 'first'
}).round(3)

campaign_summary.columns = ['customer_count', 'discount_percent', 'expected_ctr']
print(campaign_summary)

# Save campaign data
campaign_df.to_csv('data/processed/campaign_assignments.csv', index=False)

# Save campaign strategies for reference
with open('data/processed/campaign_strategies.json', 'w') as f:
    json.dump(campaign_strategies, f, indent=2)

print(f"\n✅ Campaign assignments saved to data/processed/campaign_assignments.csv")
print("✅ Step 5 completed successfully!")
print("Next: Run Step 6 (A/B Testing Setup)")
