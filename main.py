import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Load Bank Statement 1
df1 = pd.read_csv('bank_statement_1.csv', parse_dates=['Date'])

# Load Bank Statement 2
df2 = pd.read_csv('bank_statement_2.csv', parse_dates=['Date'])

# Combine both statements
combined_df = pd.concat([df1, df2])

# Extract features (for simplicity, we're using only one feature: Amount)
features = combined_df[['Amount']]

# Train KMeans model
kmeans = KMeans(n_clusters=3)
kmeans.fit(features)

# Add a new column to the DataFrame indicating the cluster
combined_df['Cluster'] = kmeans.labels_

# Get cluster centers
cluster_centers = kmeans.cluster_centers_

# Plot spending by cluster as a histogram
plt.figure(figsize=(12, 6))
plt.hist([combined_df[combined_df['Cluster'] == i]['Amount'] for i in range(3)], bins=20, stacked=True, color=['purple', 'orange', 'green'], edgecolor='black', label=['Cluster 0', 'Cluster 1', 'Cluster 2'])
plt.title('Distribution of Spending by Cluster')
plt.xlabel('Amount')
plt.ylabel('Frequency')
plt.legend()
plt.show()

# Provide advice based on cluster analysis
advice = []

for i in range(len(cluster_centers)):
    cluster_center = cluster_centers[i][0]
    
    if cluster_center > 0:
        advice.append(f"Cluster {i}: You tend to spend a lot on deposits or essential expenses. Consider optimizing your budget or finding ways to save on necessities.")
    else:
        advice.append(f"Cluster {i}: A significant portion of your spending is on non-essential items. Consider identifying areas where you can cut back to save more.")

print("Advice:")
for a in advice:
    print(a)

# Identify the month with the highest spending
combined_df['Month'] = combined_df['Date'].dt.month

# Plot monthly spending as histograms
plt.figure(figsize=(12, 6))
for month in range(1, 11):
    plt.hist(combined_df[combined_df['Month'] == month]['Amount'], bins=20, alpha=0.5, label=f'Month {month}', edgecolor='black')
plt.title('Distribution of Monthly Spending')
plt.xlabel('Amount')
plt.ylabel('Frequency')
plt.legend()
plt.show()

# Identify the month with the highest spending
highest_spending_month = combined_df.groupby('Month')['Amount'].sum().idxmax()
print(f"The month with the highest spending is: {highest_spending_month}")
