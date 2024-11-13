def load_image(image_path):
    print("Loading image...")
    with open(image_path, 'rb') as f:
        data = f.read()

    header = data[:54]
    width = header[18] + (header[19] << 8)
    height = header[22] + (header[23] << 8)

    pixels = []
    pixel_data_start = 54
    total_pixels = width * height

    for i in range(total_pixels):
        blue = data[pixel_data_start + i * 3]
        green = data[pixel_data_start + i * 3 + 1]
        red = data[pixel_data_start + i * 3 + 2]
        pixels.append((red, green, blue))

    print(f"Loaded image with width: {width}, height: {height}")
    return pixels

def calculate_distance(pixel1, pixel2):
    return sum((p1 - p2) ** 2 for p1, p2 in zip(pixel1, pixel2)) ** 0.5

def kmeans_clustering(pixels, n_clusters, max_iterations=100):
    centroids = pixels[:n_clusters]
    
    for iteration in range(max_iterations):
        clusters = [[] for _ in range(n_clusters)]
        
        for pixel in pixels:
            distances = [calculate_distance(pixel, centroid) for centroid in centroids]
            closest_centroid = distances.index(min(distances))
            clusters[closest_centroid].append(pixel)

        new_centroids = [tuple(sum(color) // len(cluster) for color in zip(*cluster)) if cluster else centroids[i] 
                         for i, cluster in enumerate(clusters)]

        if new_centroids == centroids:
            print("Convergence reached.")
            break
        centroids = new_centroids

    return centroids, clusters

def save_clusters_to_csv(clusters, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        csvfile.write("r,g,b,cluster\n")
        for cluster_index, cluster in enumerate(clusters):
            for pixel in cluster:
                csvfile.write(f"{pixel[0]},{pixel[1]},{pixel[2]},{cluster_index}\n")
    print(f"Clusters saved to {output_csv}")

def main():
    image_path = '14B_Multimedia_KMeans/image.bmp'
    n_clusters = int(input("Enter the number of clusters: "))

    pixels = load_image(image_path)
    centroids, clusters = kmeans_clustering(pixels, n_clusters)
    
    output_csv = '14B_Multimedia_KMeans/clustered_data.csv'
    save_clusters_to_csv(clusters, output_csv)

    print("Processing complete.")

if __name__ == "__main__":
    main()
