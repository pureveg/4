import csv

def create_bins(data, bin_width):
    sorted_data = sorted(data)
    return [sorted_data[i:i + bin_width] for i in range(0, len(sorted_data), bin_width)]

def min_max_normalize(value, min_val, max_val, new_min, new_max):
    return (((value - min_val) * (new_max - new_min)) / (max_val - min_val)) + new_min

def z_score_normalize(value, mean_val, std_dev):
    return (value - mean_val) / std_dev

def calculate_statistics(values):
    mean_val = sum(values) / len(values)
    std_dev = (sum((x - mean_val) ** 2 for x in values) / len(values)) ** 0.5
    return mean_val, std_dev

def read_data_from_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        return [int(value) for row in reader for value in row]

def write_normalized_csv(file_path, fieldnames, rows):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(rows)

if __name__ == "__main__":
    file_path = "3_Binning/BinningIPData.csv"
    bin_width = int(input("Enter the bin width: "))
    data = read_data_from_csv(file_path)
    
    binned_data = create_bins(data, bin_width)
    print("Binned Data:", binned_data)
    
    min_min = float(input("Enter the minimum value for normalization: "))
    max_max = float(input("Enter the maximum value for normalization: "))

    min_max_normalized_bins = []
    z_score_normalized_bins = []

    for bin_data in binned_data:
        min_val, max_val = min(bin_data), max(bin_data)
        mean_val, std_dev = calculate_statistics(bin_data)
        
        min_max_normalized_bins.append([round(min_max_normalize(value, min_val, max_val, min_min, max_max), 3) for value in bin_data])
        z_score_normalized_bins.append([round(z_score_normalize(value, mean_val, std_dev), 3) for value in bin_data])

    write_normalized_csv('3_Binning/MinMax_Normalized_Bins.csv', ['Bin' + str(i+1) for i in range(len(binned_data))], min_max_normalized_bins)
    write_normalized_csv('3_Binning/ZScore_Normalized_Bins.csv', ['Bin' + str(i+1) for i in range(len(binned_data))], z_score_normalized_bins)

    print("Normalization complete. Min-Max and Z-Score data saved.")
