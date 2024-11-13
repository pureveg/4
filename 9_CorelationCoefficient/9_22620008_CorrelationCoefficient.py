import csv

def calculate_correlation(file_path, col1_index, col2_index):
    col1, col2 = [], []

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            col1.append(float(row[col1_index]))
            col2.append(float(row[col2_index]))

    n = len(col1)
    sum_x, sum_y = sum(col1), sum(col2)
    sum_x_square, sum_y_square = sum(x**2 for x in col1), sum(y**2 for y in col2)
    sum_xy = sum(col1[i] * col2[i] for i in range(n))

    numerator = n * sum_xy - sum_x * sum_y
    denominator = ((n * sum_x_square - sum_x**2) * (n * sum_y_square - sum_y**2))**0.5

    return numerator / denominator if denominator != 0 else 0

def main():
    file_path = '9_CorelationCoefficient/data_ISE.csv'
    correlation = calculate_correlation(file_path, 1, 2)
    print(f"Correlation coefficient between ISE and S&P 500 Index (US): {correlation:.4f}")

main()
