import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure directories exist
os.makedirs('data/processed', exist_ok=True)
os.makedirs('data/results', exist_ok=True)

print("Step 4: Performing K-means clustering...")

# Load RFM data from Step 2
rfm_customers = pd.read_csv('data/processed/rfm_analysis.csv')
print(f"Loaded {len(rfm_customers)} customers for clustering")

# Prepare features for clustering
features_for_clustering = ['recency', 'frequency', 'monetary_total', 'monetary_avg', 'age']
X = rfm_customers[features_for_clustering].fillna(0)

print("Selected features for clustering:", features_for_clustering)

# Standardize features (very important for K-means!)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("Features standardized successfully")

# Find optimal number of clusters using elbow method and silhouette score
print("Finding optimal number of clusters...")

inertias = []
silhouette_scores = []
k_range = range(2, 8)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))
    print(f"k={k}: Inertia={kmeans.inertia_:.2f}, Silhouette={silhouette_score(X_scaled, kmeans.labels_):.3f}")

# Plot optimization curves
plt.figure(figsize=(15, 5))

# Elbow curve
plt.subplot(1, 3, 1)
plt.plot(k_range, inertias, 'bo-', linewidth=2, markersize=8)
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method For Optimal k')
plt.grid(True, alpha=0.3)

# Silhouette score
plt.subplot(1, 3, 2)
plt.plot(k_range, silhouette_scores, 'ro-', linewidth=2, markersize=8)
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score vs k')
plt.grid(True, alpha=0.3)

# Apply K-means with 4 clusters (as required by your resume)
print("\nApplying K-means with 4 clusters...")
kmeans_final = KMeans(n_clusters=4, random_state=42, n_init=10)
clusters = kmeans_final.fit_predict(X_scaled)

# Add cluster labels to data
rfm_customers['cluster'] = clusters

# Calculate final silhouette score
final_silhouette = silhouette_score(X_scaled, clusters)
print(f"Final silhouette score with 4 clusters: {final_silhouette:.3f}")

# Cluster visualization
plt.subplot(1, 3, 3)
scatter = plt.scatter(rfm_customers['frequency'], rfm_customers['monetary_total'], 
                     c=clusters, cmap='viridis', alpha=0.6, s=50)
plt.xlabel('Frequency (Number of Transactions)')
plt.ylabel('Monetary Total ($)')
plt.title('Customer Segments\n(Frequency vs Monetary)')
plt.colorbar(scatter)

plt.tight_layout()
plt.savefig('data/results/cluster_optimization.png', dpi=300, bbox_inches='tight')
plt.show()

# Analyze segments in detail
print("\n=== CUSTOMER SEGMENT ANALYSIS ===")

segment_analysis = rfm_customers.groupby('cluster').agg({
    'customer_id': 'count',
    'recency': 'mean',
    'frequency': 'mean',
    'monetary_total': 'mean',
    'monetary_avg': 'mean',
    'age': 'mean'
}).round(2)

segment_analysis.columns = ['customer_count', 'avg_recency', 'avg_frequency', 
                           'avg_total_spent', 'avg_order_value', 'avg_age']

print("Customer Segment Characteristics:")
print(segment_analysis)

# Define segment names based on characteristics
segment_definitions = {
    0: {
        'name': 'Champions',
        'description': 'High-value, frequent, recent customers',
        'strategy': 'Reward and retain with VIP treatment',
        'color': '#FF6B6B'
    },
    1: {
        'name': 'Loyal Customers', 
        'description': 'Regular customers with good monetary value',
        'strategy': 'Upsell and cross-sell opportunities',
        'color': '#4ECDC4'
    },
    2: {
        'name': 'At Risk',
        'description': 'Previously valuable but haven\'t purchased recently',
        'strategy': 'Win-back campaigns with special offers',
        'color': '#45B7D1'
    },
    3: {
        'name': 'Potential Loyalists',
        'description': 'Recent customers with good frequency',
        'strategy': 'Nurture relationship with targeted content',
        'color': '#96CEB4'
    }
}

# Add segment names and strategies to data
rfm_customers['segment_name'] = rfm_customers['cluster'].map(lambda x: segment_definitions[x]['name'])
rfm_customers['segment_description'] = rfm_customers['cluster'].map(lambda x: segment_definitions[x]['description'])
rfm_customers['segment_strategy'] = rfm_customers['cluster'].map(lambda x: segment_definitions[x]['strategy'])

# Print segment summary
print("\nSegment Definitions:")
for cluster_id, details in segment_definitions.items():
    count = len(rfm_customers[rfm_customers['cluster'] == cluster_id])
    percentage = (count / len(rfm_customers)) * 100
    print(f"\nCluster {cluster_id} - {details['name']}: {count} customers ({percentage:.1f}%)")
    print(f"  Description: {details['description']}")
    print(f"  Strategy: {details['strategy']}")

# Save final segmented data
rfm_customers.to_csv('data/processed/customer_segments.csv', index=False)
print(f"\n✅ Customer segments saved to data/processed/customer_segments.csv")

# Save segment definitions for later use
import json
with open('data/processed/segment_definitions.json', 'w') as f:
    json.dump(segment_definitions, f, indent=2)

print("✅ Step 4 completed successfully!")
print("Next: Run Step 5 (Marketing Strategy Development)")
