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
    return math.log(x, base)

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

def gini_index(data):
    labels = [row[-1] for row in data]
    label_counts = {}
    for label in labels:
        label_counts[label] = label_counts.get(label, 0) + 1
    
    gini_value = 1.0
    total_count = len(data)
    for count in label_counts.values():
        probability = count / total_count
        gini_value -= probability ** 2
    
    return gini_value

def information_gain(data, feature_index):
    total_entropy = entropy(data)
    
    feature_values = {}
    for row in data:
        value = row[feature_index]
        if value not in feature_values:
            feature_values[value] = []
        feature_values[value].append(row)
    
    weighted_entropy = 0
    for subset in feature_values.values():
        weighted_entropy += (len(subset) / len(data)) * entropy(subset)

    return total_entropy - weighted_entropy

def gini_index_per_feature(data, feature_index):
    feature_values = {}
    for row in data:
        value = row[feature_index]
        if value not in feature_values:
            feature_values[value] = []
        feature_values[value].append(row)
    
    weighted_gini = 0
    total_count = len(data)
    for subset in feature_values.values():
        weighted_gini += (len(subset) / total_count) * gini_index(subset)
        
    return weighted_gini

if __name__ == "__main__":
    feature_names, data = importdata(path="4_InfoGain/Table1.csv")
    
    initial_entropy = entropy(data)
    print(f"\nInitial Entropy of dataset: {initial_entropy:.3f}\n")
    
    print("Information Gain and Gini Index for each feature:")
    
    for feature_index in range(len(feature_names) - 1): 
        ig = information_gain(data, feature_index)
        gi = gini_index_per_feature(data, feature_index)        
        print(f"Feature '{feature_names[feature_index]}': Information Gain = {ig:.3f}, Gini Index = {gi:.3f}\n")
