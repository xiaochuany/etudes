import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist

st.set_page_config(layout="centered", page_title="Clustering Demo")

@st.cache_data
def get_clustering_data(n_samples=20, n_clusters=5):
    np.random.seed(0)
    data_points = []
    for _ in range(n_clusters):
        center = np.random.uniform(-10, 10, 2)
        cluster_points = np.random.randn(n_samples // n_clusters, 2) * 1.5 + center
        data_points.append(cluster_points)
    data = np.vstack(data_points)
    n_points = len(data)

    Z = linkage(pdist(data), method='ward')

    all_labels = {}
    merged_points_info = {}
    assignments = np.arange(n_points + len(Z), dtype=int)
    
    for i in range(len(Z)):
        # Get clusters being merged at this step
        c1, c2 = int(Z[i, 0]), int(Z[i, 1])
        new_c = n_points + i
        
        # Store which original points are in the clusters being merged *at this step*
        points_in_merge = np.where((assignments[:n_points] == c1) | (assignments[:n_points] == c2))[0]
        merged_points_info[i] = points_in_merge

        # Update assignments for the next step
        mask = (assignments == c1) | (assignments == c2)
        assignments[mask] = new_c
        
        # Store final labels for the original points at this step
        current_point_assignments = assignments[:n_points]
        # Map cluster IDs to a consecutive range (0, 1, 2...) for consistent coloring
        _unique_clusters, labels = np.unique(current_point_assignments, return_inverse=True)
        all_labels[i] = labels

    return data, Z, all_labels, merged_points_info

# --- Main App ---

st.title("Hierarchical Clustering Demo")

data, Z, all_labels, merged_points = get_clustering_data()
n_points = len(data)
max_steps = len(Z)

step = st.slider(
    "Merge Step Control",
    min_value=1,
    max_value=max_steps
)

# brief current merge step
merge_info = Z[step-1]
info_text = (f"**Step {step}/{max_steps}:** "
             f"Merging clusters `{int(merge_info[0])}` and `{int(merge_info[1])}` "
             f"at distance `{merge_info[2]:.2f}`.")
st.markdown(info_text)

#  plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
plt.style.use('seaborn-v0_8-whitegrid')

# 1. Dendrogram
dendrogram(Z, ax=ax1, color_threshold=Z[step-1, 2], above_threshold_color='gray')
ax1.set_title("Dendrogram")
ax1.set_xlabel("Data Point or Cluster Index")
ax1.set_ylabel("Distance")
ax1.axhline(y=Z[step-1, 2], c='r', lw=2, linestyle='--')
ax1.annotate('Current Merge', xy=(0, Z[step-1, 2]), xytext=(10, Z[step-1, 2] + Z.max()/10),
             arrowprops=dict(facecolor='red', shrink=0.05), color='red')

# 2. Scatter Plot of Clusters
labels = all_labels[step-1]
num_unique_clusters = len(np.unique(labels))
cmap = plt.get_cmap('viridis', num_unique_clusters)

ax2.scatter(data[:, 0], data[:, 1], c=labels, cmap=cmap, s=50, alpha=0.8)
ax2.set_title(f"Cluster State ({num_unique_clusters} clusters)")
ax2.set_xlabel("Feature 1")
ax2.set_ylabel("Feature 2")

# Highlight points being merged in this step
points_in_merge = merged_points[step-1]
if len(points_in_merge) > 0:
    ax2.scatter(data[points_in_merge, 0], data[points_in_merge, 1], 
                s=200, facecolors='none', edgecolors='red', linewidths=2,
                label='Currently Merging')
ax2.legend(loc='upper right')

st.pyplot(fig)
