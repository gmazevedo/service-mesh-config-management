# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Load the World Happiness Report 2021 dataset
df = pd.read_csv('world-happiness-report-2021.csv')

# Select relevant features for clustering
features = df[['Logged GDP per capita', 'Social support', 'Healthy life expectancy']]

# Standardize the features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Apply K-means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(features_scaled)

pca = PCA(n_components=2)
features_pca = pca.fit_transform(features_scaled)

print(df[['Country name', 'Cluster']].to_string())

# Visualize the clusters
plt.scatter(features_pca[:, 0], features_pca[:, 1], c=df['Cluster'], cmap='viridis', alpha=0.5)
plt.title('K-means Clustering of World Happiness Report 2021')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()

