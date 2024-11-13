import csv

def load_data_from_csv(filename):
    ise = []
    sp = []
    
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            ise.append(float(row[1]))
            sp.append(float(row[2]))

    return ise, sp

def calculate_coefficients(X, y):
    n = len(X)
    X_mean = sum(X) / n
    y_mean = sum(y) / n

    num = sum((X[i] - X_mean) * (y[i] - y_mean) for i in range(n))
    den = sum((X[i] - X_mean) ** 2 for i in range(n))

    b1 = num / den
    b0 = y_mean - b1 * X_mean

    return b0, b1

def predict_y(b0, b1, x):
    return b0 + b1 * x

def main():
    input_csv = '14_Linear_Regression_Coefficient/data_ISE.csv'
    ise, sp = load_data_from_csv(input_csv)

    b0, b1 = calculate_coefficients(ise, sp)
    print(f"Intercept (b0): {b0}")
    print(f"Slope (b1): {b1}")

    x_input = float(input("Enter a value for ISE (x) to predict SP (y): "))
    predicted_y = predict_y(b0, b1, x_input)
    print(f"The predicted value of SP (y) for ISE (x) = {x_input} is: {predicted_y}")

if __name__ == "__main__":
    main()
