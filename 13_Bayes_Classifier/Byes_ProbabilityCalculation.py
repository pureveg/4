import csv

def load_data_from_csv(filename):
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        data = [row for row in reader][1:]  
    return data

def calculate_probabilities(data):
    total_cases = len(data)
    class_counts = {}
    feature_counts = {}

    for row in data:
        cls = row[-1]  
        if cls not in class_counts:
            class_counts[cls] = 0
            feature_counts[cls] = {}
        class_counts[cls] += 1

        for feature_index in range(len(row) - 1):
            feature_value = row[feature_index]
            if feature_value not in feature_counts[cls]:
                feature_counts[cls][feature_value] = 0
            feature_counts[cls][feature_value] += 1

    probabilities = {}
    for cls, count in class_counts.items():
        probabilities[cls] = {'prior': count / total_cases}
        for feature_value, feature_count in feature_counts[cls].items():
            probabilities[cls][feature_value] = (feature_count + 1) / (count + len(feature_counts[cls]))  # Applying Laplace Smoothing

    return probabilities

def write_probabilities_to_file(probabilities, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Class", "Feature", "Probability"])
        
        for cls, probs in probabilities.items():
            for feature_value, prob in probs.items():
                if feature_value != 'prior':
                    writer.writerow([cls, feature_value, prob])
            writer.writerow([cls, 'Prior', probs['prior']])

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

    outlook_choice = int(input("Select the Outlook (1: sunny, 2: overcast, 3: rain): ")) - 1
    temperature_choice = int(input("Select the Temperature (1: hot, 2: mild, 3: cool): ")) - 1
    humidity_choice = int(input("Select the Humidity (1: high, 2: normal): ")) - 1
    windy_choice = int(input("Select Windy (1: true, 2: false): ")) - 1

    unknown_case = [
        outlook_options[outlook_choice],
        temperature_options[temperature_choice],
        humidity_options[humidity_choice],
        windy_options[windy_choice]
    ]

    return unknown_case

def main():
    input_csv = '13_Bayes_Classifier/Table1.csv'
    output_csv = 'probabilities_output.csv'

    data = load_data_from_csv(input_csv)
    probabilities = calculate_probabilities(data)

    write_probabilities_to_file(probabilities, output_csv)

    unknown_case = get_user_input()

    predicted_class = predict(probabilities, unknown_case)

    print(f"\nPredicted class for the unknown case: {predicted_class}")

if __name__ == "__main__":
    main()
