import csv

def read_csv(input_file):
    data = []
    with open(input_file, mode='r') as file:
        csvreader = csv.reader(file)
        headers = next(csvreader)
        for row in csvreader:
            data.append([float(value) for value in row])
    return data, headers

def write_csv(output_file, data, headers):
    with open(output_file, mode='w', newline='') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(headers + ['Cluster'])
        for row in data:
            csvwriter.writerow(row)

def euclidean_distance(point1, point2):
    return sum((x - y) ** 2 for x, y in zip(point1, point2)) ** 0.5

def manhattan_distance(point1, point2):
    return sum(abs(x - y) for x, y in zip(point1, point2))

def chebyshev_distance(point1, point2):
    return max(abs(x - y) for x, y in zip(point1, point2))

def initialize_centroids(data, k):
    unique_data = []
    for point in data:
        if point not in unique_data:
            unique_data.append(point)
        if len(unique_data) == k:
            break
    return unique_data[:k]

def assign_clusters(data, centroids, distance_func):
    clusters = []
    for point in data:
        distances = [distance_func(point, centroid) for centroid in centroids]
        cluster = distances.index(min(distances))
        clusters.append(cluster)
    return clusters

def update_centroids(data, clusters, k):
    new_centroids = []
    for i in range(k):
        cluster_points = [data[j] for j in range(len(data)) if clusters[j] == i]
        if cluster_points:
            centroid = [sum(dim) / len(dim) for dim in zip(*cluster_points)]
            new_centroids.append(centroid)
        else:
            new_centroids.append(data[0])
    return new_centroids

def kmeans_clustering(input_csv, output_csv, k, distance_func, max_iters=100):
    data, headers = read_csv(input_csv)
    centroids = initialize_centroids(data, k)
    
    print("Initial centroids:", centroids)
    
    for iteration in range(max_iters):
        print(f"\nIteration {iteration + 1}")
        clusters = assign_clusters(data, centroids, distance_func)
        new_centroids = update_centroids(data, clusters, k)
        
        print("Updated centroids:", new_centroids)
        
        if new_centroids == centroids:
            print("Convergence reached, stopping iterations.")
            break
        
        centroids = new_centroids
    
    for i, row in enumerate(data):
        row.append(clusters[i])
    
    write_csv(output_csv, data, headers)
    print(f'Clustering result saved to {output_csv}')

    print("\nFinal centroids:", centroids)

input_csv = '10_KmeansClustering/circleData.csv'
output_csv = '10_KmeansClustering/Cluster_Distances.csv'
k = int(input("Enter the number of clusters: "))

print("Select distance formula:")
print("1. Euclidean Distance")
print("2. Manhattan Distance")
print("3. Chebyshev Distance")
choice = input("Enter the number of your choice (1/2/3): ")

if choice == '1':
    distance_function = euclidean_distance
elif choice == '2':
    distance_function = manhattan_distance
elif choice == '3':
    distance_function = chebyshev_distance
else:
    print("Invalid choice. Defaulting to Euclidean Distance.")
    distance_function = euclidean_distance

kmeans_clustering(input_csv, output_csv, k, distance_function)
