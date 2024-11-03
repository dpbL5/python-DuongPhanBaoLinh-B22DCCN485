import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import seaborn as sns
import argparse
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Read data from CSV file
data = pd.read_csv('./code/output/result.csv')

# Select necessary columns for classification
attributes = ['age', 'games', 'minutes', 'goals', 'assists', 'xg', 'npxg', 'xg_assist', 'progressive_carries', 'progressive_passes']

# Filter data to include only the selected columns
data_filtered = data[attributes].dropna()

# Standardize the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data_filtered)

# Use the elbow method to determine the optimal number of clusters
def find_optimal_clusters(data, max_k):
    iters = range(1, max_k+1)
    sse = []
    for k in iters:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(data)
        sse.append(kmeans.inertia_)
    plt.figure(figsize=(8, 6))
    plt.plot(iters, sse, marker='o')
    plt.xlabel('Cluster Centers')
    plt.ylabel('SSE')
    plt.title('Elbow Method For Optimal k')
    plt.show()

find_optimal_clusters(data_scaled, 10)

# Choose the number of clusters (e.g., 4)
kmeans = KMeans(n_clusters=4, random_state=42)
data['cluster'] = kmeans.fit_predict(data_scaled)

# Reduce data dimensions to 2D using PCA
pca = PCA(n_components=2)
data_pca = pca.fit_transform(data_scaled)
data['pca1'] = data_pca[:, 0]
data['pca2'] = data_pca[:, 1]

# Plot the clusters on a 2D plane
plt.figure(figsize=(10, 8))
sns.scatterplot(x='pca1', y='pca2', hue='cluster', data=data, palette='viridis')
plt.title('K-means Clustering with PCA')
plt.show()

# Function to plot radar chart
def radar_chart(player1, player2, attributes):
    player1_data = data[data['player'] == player1][attributes].values.flatten().tolist()
    player2_data = data[data['player'] == player2][attributes].values.flatten().tolist()
    
    labels = attributes
    num_vars = len(labels)
    
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    player1_data += player1_data[:1]
    player2_data += player2_data[:1]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, player1_data, color='blue', alpha=0.25)
    ax.fill(angles, player2_data, color='red', alpha=0.25)
    ax.plot(angles, player1_data, color='blue', linewidth=2, label=player1)
    ax.plot(angles, player2_data, color='red', linewidth=2, label=player2)
    
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Radar Chart Plotter')
    parser.add_argument('--p1', type=str, required=True, help='Player Name 1')
    parser.add_argument('--p2', type=str, required=True, help='Player Name 2')
    parser.add_argument('--Attribute', type=str, required=True, help='Attributes to compare, separated by commas')
    
    args = parser.parse_args()
    player1 = args.p1
    player2 = args.p2
    attributes = args.Attribute.split(',')
    
    radar_chart(player1, player2, attributes)
