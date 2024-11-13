import csv

def read_csv(input_file):
    data = []
    with open(input_file, mode='r') as file:
        csvreader = csv.reader(file)
        headers = next(csvreader)
        for row in csvreader:
            # Only take the first two columns for clustering
            data.append([float(row[0]), float(row[1])])
    
    num_attributes = len(data[0])  # Should always be 2 after this change
    print(f"Dimensionality of the data: {num_attributes}D")
    return data, headers[:2]  # Return only the first two headers

def write_csv(output_file, data, headers):
    with open(output_file, mode='w', newline='') as file:
        csvwriter = csv.writer(file)
        # Write only the first two headers
        csvwriter.writerow(headers + ['Cluster'])
        for row in data:
            formatted_row = [f"{value:.3f}" for value in row]
            csvwriter.writerow(formatted_row)

def euclidean_distance(point1, point2):
    return sum((x - y) ** 2 for x, y in zip(point1, point2)) ** 0.5

def region_query(data, point_idx, epsilon):
    neighbors = []
    for i, point in enumerate(data):
        if euclidean_distance(data[point_idx], point) <= epsilon:
            neighbors.append(i)
    return neighbors

def expand_cluster(data, point_idx, neighbors, cluster, epsilon, min_pts, visited, clusters):
    cluster[point_idx] = len(clusters)
    visited[point_idx] = True
    
    i = 0
    while i < len(neighbors):
        point = neighbors[i]
        if not visited[point]:
            visited[point] = True
            point_neighbors = region_query(data, point, epsilon)
            if len(point_neighbors) >= min_pts:
                neighbors.extend(point_neighbors)
        if point not in cluster:
            cluster[point] = len(clusters)
        i += 1

def dbscan(data, epsilon, min_pts):
    visited = [False] * len(data)
    cluster = [-1] * len(data)
    clusters = []
    
    for point_idx in range(len(data)):
        if not visited[point_idx]:
            visited[point_idx] = True
            neighbors = region_query(data, point_idx, epsilon)
            if len(neighbors) >= min_pts:
                clusters.append([])
                expand_cluster(data, point_idx, neighbors, cluster, epsilon, min_pts, visited, clusters)
            else:
                cluster[point_idx] = -1
    return cluster

def dbscan_clustering(input_csv, output_csv, epsilon, min_pts):
    data, headers = read_csv(input_csv)
    
    clusters = dbscan(data, epsilon, min_pts)
    
    for i, row in enumerate(data):
        row.append(clusters[i])
    
    write_csv(output_csv, data, headers)
    
    print("\nResults:")
    for i, row in enumerate(data):
        formatted_values = [f"{value:.3f}" for value in row[:-1]]
        point_type = "Noise" if clusters[i] == -1 else f"Cluster {clusters[i]}"
        print(f"Value: {formatted_values} -> {point_type}")

    print(f"\nClustering result saved to {output_csv}")

input_csv = 'Mine_Dataset_CSV.csv'  
output_csv = 'Clustering_DensityBased.csv'
epsilon = 0.5  
min_pts = 3  

dbscan_clustering(input_csv, output_csv, epsilon, min_pts)
