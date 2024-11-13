import csv

def read_csv(input_file):
    with open(input_file, mode='r') as file:
        csvreader = csv.reader(file)
        headers = next(csvreader)
        data = [[float(value) for value in row] for row in csvreader]
    return data, headers

def write_csv(output_file, data, headers):
    with open(output_file, mode='w', newline='') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(headers + ['Distance'])
        for row in data:
            csvwriter.writerow([f"{value:.3f}" for value in row])

def write_distance_matrix(output_file, distance_matrix):
    with open(output_file, 'w') as file:
        for row in distance_matrix:
            file.write(' '.join(f"{value:.3f}" for value in row) + '\n')

def euclidean_distance(point1, point2):
    return sum((x - y) ** 2 for x, y in zip(point1, point2)) ** 0.5

def manhattan_distance(point1, point2):
    return sum(abs(x - y) for x, y in zip(point1, point2))

def chebyshev_distance(point1, point2):
    return max(abs(x - y) for x, y in zip(point1, point2))

def compute_centroid(data):
    n = len(data)
    dimensions = len(data[0])
    centroid = [sum(point[i] for point in data) / n for i in range(dimensions)]
    return centroid

def compute_distance_matrix(data, centroid, distance_func):
    n = min(len(data), 10)
    distance_matrix = []
    
    for i in range(n):
        row = []
        for j in range(i + 1):
            if i == j:
                distance = distance_func(data[i], centroid)
            else:
                distance = distance_func(data[i], data[j])
            row.append(round(distance, 3))
        distance_matrix.append(row)
    
    return distance_matrix

def cluster_analysis(input_csv, output_csv, distance_func):
    data, headers = read_csv(input_csv)
    
    centroid = compute_centroid(data)
    print("Cluster centroid:", [f"{value:.3f}" for value in centroid])
    
    for i in range(len(data)):
        distance = distance_func(data[i], centroid)
        data[i].append(round(distance, 3))
    
    write_csv(output_csv, data, headers)
    print(f"Results saved to {output_csv}")

    distance_matrix = compute_distance_matrix(data, centroid, distance_func)
    print("\nLower Triangular Matrix of Distances for First 10 Rows:")
    
    write_distance_matrix("distance_matrix.txt", distance_matrix)
    print("Lower triangular matrix saved to distance_matrix.txt")

input_csv = '10_KmeansClustering/circleData.csv'
output_csv = '10_KmeansClustering/Cluster_Distances.csv'

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

cluster_analysis(input_csv, output_csv, distance_function)
