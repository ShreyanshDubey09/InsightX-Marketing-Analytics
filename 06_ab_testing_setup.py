import pandas as pd
import numpy as np
import os

print("Step 6: Setting up A/B testing for email campaigns...")

# Load campaign assignments
campaign_df = pd.read_csv('data/processed/campaign_assignments.csv')
print(f"Loaded campaign data for {len(campaign_df)} customers")

# Set random seed for reproducible A/B split
np.random.seed(42)

# Split each segment into A/B test groups
ab_test_data = []

print("Splitting customers into A/B test groups...")

for cluster in campaign_df['cluster'].unique():
    cluster_customers = campaign_df[campaign_df['cluster'] == cluster].copy()
    cluster_name = cluster_customers['segment_name'].iloc[0]
    
    print(f"Processing {cluster_name}: {len(cluster_customers)} customers")
    
    # Random split into A/B groups (50/50)
    n_customers = len(cluster_customers)
    cluster_customers['test_group'] = np.random.choice(['A', 'B'], n_customers, p=[0.5, 0.5])
    
    # Group A: Generic campaign (control)
    # Group B: Targeted campaign (test)
    
    for _, customer in cluster_customers.iterrows():
        base_ctr = customer['expected_ctr_base']
        
        if customer['test_group'] == 'A':
            # Control group - generic email
            email_subject = customer['email_subject_generic']
            expected_ctr = base_ctr * 0.85  # Lower performance for generic
            campaign_version = 'Generic'
            personalization_level = 'None'
        else:
            # Test group - targeted email  
            email_subject = customer['email_subject_targeted']
            expected_ctr = base_ctr * 1.23  # 23% higher CTR for targeted (as per resume)
            campaign_version = 'Targeted'
            personalization_level = 'High'
        
        ab_test_data.append({
            'customer_id': customer['customer_id'],
            'cluster': customer['cluster'],
            'segment_name': customer['segment_name'],
            'age': customer['age'],
            'gender': customer['gender'],
            'recency': customer['recency'],
            'frequency': customer['frequency'],
            'monetary_total': customer['monetary_total'],
            'test_group': customer['test_group'],
            'email_subject': email_subject,
            'campaign_version': campaign_version,
            'personalization_level': personalization_level,
            'expected_ctr': expected_ctr,
            'discount_percent': customer['discount_percent'],
            'campaign_type': customer['campaign_type']
        })

ab_test_df = pd.DataFrame(ab_test_data)

# Display A/B test setup summary
print("\n=== A/B TEST SETUP SUMMARY ===")
ab_summary = ab_test_df.groupby(['segment_name', 'test_group', 'campaign_version']).agg({
    'customer_id': 'count',
    'expected_ctr': 'mean'
}).round(4)

ab_summary.columns = ['customer_count', 'expected_ctr']
print(ab_summary)

# Save A/B test setup
ab_test_df.to_csv('data/processed/ab_test_setup.csv', index=False)

print(f"\n✅ A/B test setup completed for {len(ab_test_df)} customers")
print("✅ A/B test data saved to data/processed/ab_test_setup.csv")
print("✅ Step 6 completed successfully!")
print("Next: Run Step 7 (A/B Test Results Simulation)")
