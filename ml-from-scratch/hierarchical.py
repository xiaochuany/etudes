import marimo

__generated_with = "0.13.15"
app = marimo.App(width="columns")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        """
    # hierarchical clustering 

    init: 

    - clusters as mapping  
    - distances as heap and map

    loop:.

    1. retrieve smallest distance
    1. merge: update cluster map 
    1. compute distances of clusters with merged: update distamnce heap, update distance map
    """
    )
    return


@app.cell
def _():
    import math 
    import heapq

    def euclid(u,v):
        return math.sqrt(sum((ui-vi)**2 for ui,vi in zip(u,v)))

    def init(arr):
        """space O(m^2)"""
        m = len(arr)
        clusters = {i:{i} for i in range(m)}
        dmap = {(i,j): euclid(arr[i],arr[j])
            for i in range(m-1)
            for j in range(i+1,m)
        }
        dheap = [(d,i,j) for (i,j), d in dmap.items()]
        heapq.heapify(dheap)
        return clusters, dmap, dheap

    def main(arr, low):
        """time O(m^2 log m)"""
        clusters, dmap, dheap = init(arr)
        res = []
        while len(clusters)>low:
            # retrieve smallest
            while True: 
                d, i, j = heapq.heappop(dheap)
                if i in clusters and j in clusters:
                    break
            res.append((i,j, d, len(clusters[i])+len(clusters[j])))
            # update clusters: + 1 - 2
            new_idx = max(clusters) + 1
            clusters.update({new_idx: clusters[i].union(clusters[j])})
            clusters.pop(i)
            clusters.pop(j)
            # compute distance
            for k in clusters:
                if k != new_idx:
                    # update dmap O(1)
                    dmap[(k,new_idx)] = newtok = min(
                        dmap[tuple(sorted([i,k]))],  
                        dmap[tuple(sorted([j,k]))]
                    )
                    # udpate dheap O(log m)
                    heapq.heappush(dheap,(newtok,k,new_idx))
        return clusters, res

    return (main,)


@app.cell
def _(main):
    import numpy as np
    from scipy.cluster.hierarchy import linkage

    def test_main():
        x = np.random.standard_t(df=2, size=(100,2))
        _, Z = main(x,1)
        Z = np.asarray(Z)
        Z_scipy = linkage(x)
        np.testing.assert_allclose(Z_scipy, Z) 
    return linkage, np


@app.cell
def _(linkage, np):
    from scipy.spatial.distance import pdist

    def get_clustering_data(n_samples=20, n_clusters=5):
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
        assignments = np.arange(n_points + len(Z))

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

    return (get_clustering_data,)


@app.cell
def _(get_clustering_data, mo):
    data, Z, all_labels, merged_points = get_clustering_data()
    n_points = len(data)
    max_steps = len(Z)
    slider = mo.ui.slider(1,max_steps)
    return Z, all_labels, data, max_steps, merged_points, slider


@app.cell
def _(Z, max_steps, slider):
    step = slider.value
    merge_info = Z[step-1]
    info_text = (f"**Step {step}/{max_steps}:** "
                 f"Merging clusters `{int(merge_info[0])}` and `{int(merge_info[1])}` "
                 f"at distance `{merge_info[2]:.2f}`.")
    return (step,)


@app.cell
def _(Z, all_labels, data, merged_points, np, step):
    import matplotlib.pyplot as plt
    from scipy.cluster.hierarchy import dendrogram
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
    return


@app.cell
def _(slider):
    slider
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
