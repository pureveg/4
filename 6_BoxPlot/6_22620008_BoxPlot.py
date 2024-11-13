import csv

def read_column_values(filename, column_name):
    values = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            values.append(float(row[column_name]))  
    return sorted(values)

def calculate_quartiles(data):
    n = len(data)
    
    def get_quartile_position(frac):
        pos = (n - 1) * frac
        if pos.is_integer():
            return data[int(pos)]
        else:
            l = int(pos)
            return (data[l] + data[l + 1]) / 2

    Q1 = get_quartile_position(0.25)
    Q3 = get_quartile_position(0.75)
    return Q1, Q3

def calculate_median(data):
    n = len(data)
    mid = n // 2
    return (data[mid - 1] + data[mid]) / 2 if n % 2 == 0 else data[mid]

filename = '6_BoxPlot/data_ISE.csv'
open_values = read_column_values(filename, 'close')

Q1, Q3 = calculate_quartiles(open_values)
median = calculate_median(open_values)
min_val = min(open_values)
max_val = max(open_values)
IQR = Q3 - Q1

lower_whisker = max(Q1 - 1.5 * IQR, min_val)
upper_whisker = min(Q3 + 1.5 * IQR, max_val)

print("5 Number Summary for 'close':")
print(f"Minimum: {min_val:.3f}")
print(f"Lower Whisker: {lower_whisker:.3f}")
print(f"Q1: {Q1:.3f}")
print(f"Median: {median:.3f}")
print(f"Q3: {Q3:.3f}")
print(f"Upper Whisker: {upper_whisker:.3f}")
print(f"Maximum: {max_val:.3f}")
print(f"IQR: {IQR:.3f}")
