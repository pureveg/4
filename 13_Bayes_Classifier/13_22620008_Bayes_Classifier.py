import csv

def load_data_from_csv(filename):
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        return [row for row in reader][1:]

def calculate_probabilities(data):
    total_cases = len(data)
    class_counts = {}
    feature_counts = {}

    for row in data:
        cls = row[-1]
        class_counts[cls] = class_counts.get(cls, 0) + 1
        if cls not in feature_counts:
            feature_counts[cls] = {}

        for feature_index in range(len(row) - 1):
            feature_value = row[feature_index]
            feature_counts[cls][feature_value] = feature_counts[cls].get(feature_value, 0) + 1

    probabilities = {}
    for cls, count in class_counts.items():
        probabilities[cls] = {'prior': count / total_cases}
        for feature_value, feature_count in feature_counts[cls].items():
            probabilities[cls][feature_value] = feature_count / count

    return probabilities

def predict(probabilities, unknown_case):
    max_prob = -1
    predicted_class = None

    for cls, probs in probabilities.items():
        prob = probs['prior']
        for feature in unknown_case:
            prob *= probs.get(feature, 1e-5)

        if prob > max_prob:
            max_prob = prob
            predicted_class = cls

    return predicted_class

def get_user_input():
    outlook_options = ["sunny", "overcast", "rain"]
    temperature_options = ["hot", "mild", "cool"]
    humidity_options = ["high", "normal"]
    windy_options = [True, False]

    print("Select the Outlook: 1. sunny 2. overcast 3. rain")
    outlook_choice = int(input("Enter choice: ")) - 1
    print("Select the Temperature: 1. hot 2. mild 3. cool")
    temperature_choice = int(input("Enter choice: ")) - 1
    print("Select the Humidity: 1. high 2. normal")
    humidity_choice = int(input("Enter choice: ")) - 1
    print("Select Windy: 1. true 2. false")
    windy_choice = int(input("Enter choice: ")) - 1

    return [
        outlook_options[outlook_choice],
        temperature_options[temperature_choice],
        humidity_options[humidity_choice],
        windy_options[windy_choice]
    ]

def main():
    input_csv = '13_Bayes_Classifier/Table1.csv'
    data = load_data_from_csv(input_csv)
    probabilities = calculate_probabilities(data)
    unknown_case = get_user_input()
    predicted_class = predict(probabilities, unknown_case)
    print(f"The predicted class for the unknown case is: {predicted_class}")

if __name__ == "__main__":
    main()
