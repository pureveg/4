import csv

def min_max_normalize(value, min_val, max_val, new_min, new_max):
    return (((value - min_val) * (new_max - new_min)) / (max_val - min_val)) + new_min

def z_score_normalize(value, mean_val, std_dev):
    return (value - mean_val) / std_dev

def read_csv(file_path):
    with open(file_path, mode='r') as file:
        return list(csv.DictReader(file))

def write_csv(file_path, fieldnames, rows):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(rows)

def calculate_statistics(values):
    mean_val = sum(values) / len(values)
    std_dev = (sum((x - mean_val) ** 2 for x in values) / len(values)) ** 0.5
    return mean_val, std_dev

input_file = '2_Normalisation/Mine_Dataset_CSV.csv'
new_min = float(input("Enter the minimum value for normalization: "))
new_max = float(input("Enter the maximum value for normalization: "))

rows = read_csv(input_file)
columns = rows[0].keys()
min_max_normalized_rows = []
z_score_normalized_rows = []

for column in columns:
    values = [float(row[column]) for row in rows]
    min_val, max_val = min(values), max(values)
    mean_val, std_dev = calculate_statistics(values)

    min_max_normalized_rows.append([round(min_max_normalize(float(row[column]), min_val, max_val, new_min, new_max), 3) for row in rows])
    z_score_normalized_rows.append([round(z_score_normalize(float(row[column]), mean_val, std_dev), 3) for row in rows])

write_csv('2_Normalisation/MinMax_Normalisation_OP.csv', [f"{col}_MinMaxNormalized" for col in columns], zip(*min_max_normalized_rows))
write_csv('2_Normalisation/ZScore_Normalisation_OP.csv', [f"{col}_ZScoreNormalized" for col in columns], zip(*z_score_normalized_rows))

print("Normalization complete. Min-Max and Z-Score data saved.")
