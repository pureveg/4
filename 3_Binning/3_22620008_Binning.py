import csv

def create_bins(data, bin_width):
    sorted_data = sorted(data)
    return [sorted_data[i:i + bin_width] for i in range(0, len(sorted_data), bin_width)]

def calculate_mean(bin_data):
    return sum(bin_data) / len(bin_data) if bin_data else 0

def calculate_median(bin_data):
    n = len(bin_data)
    sorted_bin = sorted(bin_data)
    if n == 0:
        return 0
    return (sorted_bin[n // 2] + sorted_bin[-(n + 1) // 2]) / 2

def calculate_boundaries(bin_data):
    return min(bin_data), max(bin_data)

def nearest_boundary(bin_data, boundaries):
    return [min(boundaries, key=lambda b: abs(b - value)) for value in bin_data]

def read_data_from_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        return [int(value) for row in reader for value in row]

if __name__ == "__main__":
    file_path = "3_Binning/BinningIPData.csv"
    bin_width = int(input("Enter the bin width: "))
    data = read_data_from_csv(file_path)
    binned_data = create_bins(data, bin_width)

    smoothed_mean_bins = [[calculate_mean(bin_data)] * len(bin_data) for bin_data in binned_data]
    smoothed_median_bins = [[calculate_median(bin_data)] * len(bin_data) for bin_data in binned_data]
    smoothed_boundary_bins = [nearest_boundary(bin_data, calculate_boundaries(bin_data)) for bin_data in binned_data]

    print("Original Data:", data)
    print("Binned Data:", binned_data)
    print("Smoothed Data by Bin Mean:", smoothed_mean_bins)
    print("Smoothed Data by Bin Median:", smoothed_median_bins)
    print("Smoothed Data by Bin Boundaries:", smoothed_boundary_bins)
