import pandas as pd
import numpy as np
import os

print("Step 9: Preparing data for Power BI dashboard...")

# Create powerbi directory
os.makedirs('powerbi', exist_ok=True)

# Load all data files
customer_segments = pd.read_csv('data/processed/customer_segments.csv')
ab_results = pd.read_csv('data/results/ab_test_results.csv')
performance_metrics = pd.read_csv('data/results/campaign_performance_metrics.csv')

print("Loaded all data files for Power BI preparation")

# 1. Main dashboard data - combine everything
main_data = customer_segments.merge(
    ab_results[['customer_id', 'test_group', 'campaign_version', 'clicked', 'converted', 'purchase_amount']],
    on='customer_id',
    how='left'
)

# Add calculated fields for Power BI
main_data['revenue_per_customer'] = main_data['purchase_amount']
main_data['customer_lifetime_value'] = main_data['monetary_total'] * 2.5  # Estimated LTV multiplier
main_data['engagement_score'] = (
    (main_data['frequency'] / main_data['frequency'].max() * 40) +
    (main_data['monetary_total'] / main_data['monetary_total'].max() * 40) +
    ((365 - main_data['recency']) / 365 * 20)
).round(1)

# Save main dashboard data
main_data.to_csv('powerbi/dashboard_main_data.csv', index=False)
print("✅ Main dashboard data saved to powerbi/dashboard_main_data.csv")

# 2. Performance summary for KPIs
summary_data = performance_metrics.copy()
summary_data['cost_per_acquisition'] = (
    summary_data['total_costs'] / summary_data['total_conversions']
).round(2)
summary_data['revenue_per_click'] = (
    summary_data['total_revenue'] / summary_data['total_clicks']
).round(2)

summary_data.to_csv('powerbi/performance_summary.csv', index=False)
print("✅ Performance summary saved to powerbi/performance_summary.csv")

# 3. Daily performance data for time series
np.random.seed(42)
date_range = pd.date_range('2024-11-01', '2024-12-31', freq='D')
daily_data = []

for date in date_range:
    for segment in customer_segments['segment_name'].unique():
        for test_group in ['A', 'B']:
            base_performance = {
                'Champions': {'emails': 150, 'ctr_base': 0.12},
                'Loyal Customers': {'emails': 120, 'ctr_base': 0.09},
                'At Risk': {'emails': 90, 'ctr_base': 0.06},
                'Potential Loyalists': {'emails': 110, 'ctr_base': 0.08}
            }
            
            emails_sent = np.random.poisson(base_performance[segment]['emails'])
            
            if test_group == 'A':
                ctr = base_performance[segment]['ctr_base'] * 0.85
            else:
                ctr = base_performance[segment]['ctr_base'] * 1.23
                
            clicks = int(emails_sent * ctr * np.random.uniform(0.8, 1.2))
            conversions = int(clicks * 0.25 * np.random.uniform(0.8, 1.2))
            revenue = conversions * np.random.uniform(50, 200)
            
            daily_data.append({
                'date': date,
                'segment_name': segment,
                'test_group': test_group,
                'campaign_version': 'Generic' if test_group == 'A' else 'Targeted',
                'emails_sent': emails_sent,
                'clicks': clicks,
                'conversions': conversions,
                'revenue': round(revenue, 2),
                'ctr': round(clicks/emails_sent if emails_sent > 0 else 0, 4),
                'conversion_rate': round(conversions/clicks if clicks > 0 else 0, 4)
            })

daily_performance = pd.DataFrame(daily_data)
daily_performance.to_csv('powerbi/daily_performance.csv', index=False)
print("✅ Daily performance data saved to powerbi/daily_performance.csv")

# 4. Customer segment details for drill-down
segment_details = customer_segments.groupby('segment_name').agg({
    'customer_id': 'count',
    'age': 'mean',
    'recency': 'mean',
    'frequency': 'mean',
    'monetary_total': ['mean', 'sum'],
    'monetary_avg': 'mean'
}).round(2)

segment_details.columns = ['customer_count', 'avg_age', 'avg_recency', 
                          'avg_frequency', 'avg_total_spent', 'total_revenue', 'avg_order_value']
segment_details = segment_details.reset_index()

# Add segment characteristics
segment_details['segment_description'] = segment_details['segment_name'].map({
    'Champions': 'High-value customers with recent activity and frequent purchases',
    'Loyal Customers': 'Regular customers with consistent purchasing behavior',
    'At Risk': 'Previously valuable customers who haven\'t purchased recently',
    'Potential Loyalists': 'Recent customers with good engagement potential'
})

segment_details.to_csv('powerbi/segment_details.csv', index=False)
print("✅ Segment details saved to powerbi/segment_details.csv")

# 5. Campaign comparison data
campaign_comparison = ab_results.groupby(['segment_name', 'campaign_version']).agg({
    'customer_id': 'count',
    'clicked': ['sum', 'mean'],
    'converted': ['sum', 'mean'],
    'purchase_amount': 'sum'
}).round(4)

campaign_comparison.columns = ['customers', 'total_clicks', 'ctr', 'total_conversions', 
                              'conversion_rate', 'total_revenue']
campaign_comparison = campaign_comparison.reset_index()

campaign_comparison['cost_per_customer'] = 0.02  # Email cost
campaign_comparison['roi'] = (
    (campaign_comparison['total_revenue'] - (campaign_comparison['customers'] * 0.02)) /
    (campaign_comparison['customers'] * 0.02) * 100
).round(2)

campaign_comparison.to_csv('powerbi/campaign_comparison.csv', index=False)
print("✅ Campaign comparison data saved to powerbi/campaign_comparison.csv")

print(f"\n=== POWER BI FILES CREATED ===")
print("📁 powerbi/")
print("  ├── dashboard_main_data.csv      (Main dataset)")
print("  ├── performance_summary.csv      (KPI metrics)")
print("  ├── daily_performance.csv        (Time series)")
print("  ├── segment_details.csv          (Segment analysis)")
print("  └── campaign_comparison.csv      (A/B test results)")

print("\n✅ Step 9 completed successfully!")
print("Next: Import these files into Power BI")
