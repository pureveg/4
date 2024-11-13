import csv
import math

def importdata(path):
    data = []
    with open(path, mode='r') as file:
        csvreader = csv.reader(file)
        headers = next(csvreader)
        for row in csvreader:
            data.append(row)
    print("Dataset length:", len(data))
    print("Dataset shape:", (len(data), len(headers) if data else 0))
    return headers, data

def log(x, base):
    if x <= 0:
        return 0  
    return math.log(x) / math.log(base)

def entropy(data):
    labels = [row[-1] for row in data]
    label_counts = {}
    for label in labels:
        label_counts[label] = label_counts.get(label, 0) + 1
            
    probabilities = [count / len(data) for count in label_counts.values()]
    entropy_value = 0
    for p in probabilities:
        if p > 0:
            entropy_value -= p * log(p, 2) 
    return entropy_value

def initial_information_gain(data):
    return entropy(data)

def information_gain(data, feature_index):
    total_entropy = entropy(data)
    
    feature_values = {}
    for row in data:
        value = row[feature_index]
        if value not in feature_values:
            feature_values[value] = []
        feature_values[value].append(row)
    
    weighted_entropy = 0
    for value, subset in feature_values.items():
        subset_entropy = entropy(subset)
        weighted_entropy += (len(subset) / len(data)) * subset_entropy
        print(f"  Entropy of '{value}': {subset_entropy:.3f}")

    print(f"Entropy of feature '{feature_names[feature_index]}': {weighted_entropy:.3f}")
    ig=total_entropy - weighted_entropy
    print(f"InfoGain of '{feature_names[feature_index]}': {ig:.3f}\n")     

if __name__ == "__main__":
    feature_names, data = importdata(path="4_InfoGain/Table1.csv")
    
    initial_entropy = initial_information_gain(data)
    print(f"\nEntropy of data: {initial_entropy:.3f}\n")
    
    for feature_index in range(len(feature_names) - 1):  
        ig = information_gain(data, feature_index)