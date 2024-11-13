import csv

def write_to_file(message, output_file='output.txt'):
    with open(output_file, mode='a') as file:
        file.write(message + '\n')

def read_lower_triangular_matrix(input_file):
    matrix = []
    with open(input_file, mode='r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            matrix.append([float(val) for val in row])
    
    n = len(matrix)
    full_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            full_matrix[i][j] = matrix[i][j]
            full_matrix[j][i] = matrix[i][j]

    return full_matrix

def euclidean_distance(point1, point2):
    return sum((x - y) ** 2 for x, y in zip(point1, point2)) ** 0.5

def hierarchical_clustering(data, k, linkage_method, output_file='output.txt'):
    clusters = [[i] for i in range(len(data))]
    write_to_file("Initial clusters:", output_file)
    print_clusters_and_centroids(data, clusters, output_file)

    while len(clusters) > k:
        min_dist = float('inf')
        cluster_to_merge = (None, None)

        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                dist = compute_linkage_distance(data, clusters[i], clusters[j], linkage_method)
                if dist < min_dist:
                    min_dist = dist
                    cluster_to_merge = (i, j)

        cluster1, cluster2 = cluster_to_merge
        clusters[cluster1] = clusters[cluster1] + clusters[cluster2]
        del clusters[cluster2]
        write_to_file(f"\nClusters after merge (Clusters {cluster1} and {cluster2} merged):", output_file)
        print_clusters_and_centroids(data, clusters, output_file)

    point_cluster = [-1] * len(data)
    for cluster_id, cluster in enumerate(clusters):
        for point_idx in cluster:
            point_cluster[point_idx] = cluster_id

    return point_cluster

def compute_linkage_distance(data, cluster1, cluster2, linkage_method):
    if linkage_method == "single":
        return single_linkage(data, cluster1, cluster2)
    elif linkage_method == "average":
        return average_linkage(data, cluster1, cluster2)
    elif linkage_method == "complete":
        return complete_linkage(data, cluster1, cluster2)

def single_linkage(data, cluster1, cluster2):
    min_distance = float('inf')
    for i in cluster1:
        for j in cluster2:
            distance = euclidean_distance(data[i], data[j])
            min_distance = min(min_distance, distance)
    return min_distance

def average_linkage(data, cluster1, cluster2):
    distances = [euclidean_distance(data[i], data[j]) for i in cluster1 for j in cluster2]
    return sum(distances) / len(distances)

def complete_linkage(data, cluster1, cluster2):
    max_distance = float('-inf')
    for i in cluster1:
        for j in cluster2:
            distance = euclidean_distance(data[i], data[j])
            max_distance = max(max_distance, distance)
    return max_distance

def print_clusters_and_centroids(data, clusters, output_file='output.txt'):
    for i, cluster in enumerate(clusters):
        cluster_points = [data[idx] for idx in cluster]
        centroid = [sum(dim) / len(dim) for dim in zip(*cluster_points)]
        message = f"Cluster {i} (Centroid: {centroid})"
        write_to_file(message, output_file)

def hierarchical_clustering_main(input_csv, k, linkage_method, output_file='output.txt'):
    data = read_lower_triangular_matrix(input_csv)
    clusters = hierarchical_clustering(data, k, linkage_method, output_file)
    print(f'Clustering result saved to {output_file}', output_file)

input_csv = '11_HierarchicalClustering/matrixIP.csv'
output_file = '11_HierarchicalClustering/output.txt'

k = int(input("Enter the number of clusters: "))

print("Select linkage method:")
print("1. Single Linkage")
print("2. Average Linkage")
print("3. Complete Linkage")
choice = input("Enter the number of your choice (1/2/3): ")

linkage_method = {"1": "single", "2": "average", "3": "complete"}.get(choice, "single")

hierarchical_clustering_main(input_csv, k, linkage_method, output_file)
