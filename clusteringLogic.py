import pandas as pd

# Load network traffic data
network_data = pd.read_csv('network_traffic.csv')

# Load response card data
response_cards = pd.read_csv('response_cards.csv')

from sklearn.preprocessing import StandardScaler

# Select relevant features for clustering
features = ['frame_time', 'ip_src', 'ip_dst', 'tcp_len']
network_features = network_data[features]

# Standardize the features
scaler = StandardScaler()
network_features_scaled = scaler.fit_transform(network_features)

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics import calinski_harabasz_score

# Determine the optimal number of clusters using the Calinski-Harabasz index
def find_optimal_clusters(data, max_k):
    iters = range(2, max_k + 1)
    sse = []
    ch_scores = []

    for k in iters:
        kmeans = KMeans(n_clusters=k, random_state=42).fit(data)
        sse.append(kmeans.inertia_)
        ch_scores.append(calinski_harabasz_score(data, kmeans.labels_))

    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    ax1.plot(iters, sse, '-o')
    ax1.set(xlabel='Cluster Centers', ylabel='SSE', title='Elbow Method')
    ax2.plot(iters, ch_scores, '-o')
    ax2.set(xlabel='Cluster Centers', ylabel='Calinski-Harabasz Score', title='Calinski-Harabasz Index')
    plt.show()

find_optimal_clusters(network_features_scaled, 10)

# Assume the optimal number of clusters is found to be k
k = 3
kmeans = KMeans(n_clusters=k, random_state=42)
clusters = kmeans.fit_predict(network_features_scaled)
network_data['cluster'] = clusters

# Aggregate network data by day and cluster
network_summary = network_data.groupby(['day', 'cluster']).size().reset_index(name='count')

# Aggregate response card data by day
response_summary = response_cards.groupby('day').size().reset_index(name='count')

# Merge and compare
comparison = pd.merge(network_summary, response_summary, on='day', how='outer', suffixes=('_network', '_response'))
comparison['difference'] = comparison['count_response'] - comparison['count_network']

# Display inconsistencies
inconsistencies = comparison[comparison['difference'] != 0]
print(inconsistencies)
