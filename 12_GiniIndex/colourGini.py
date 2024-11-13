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

def gini_index_per_feature(data, feature_index):
    feature_values = {}
    for row in data:
        value = row[feature_index]
        if value not in feature_values:
            feature_values[value] = []
        feature_values[value].append(row)
    
    weighted_gini = {}
    total_count = len(data)
    
    for value, subset in feature_values.items():
        weighted_gini[value] = gini_index(subset)
        
    return weighted_gini

if __name__ == "__main__":
    feature_names, data = importdata(path="12_GiniIndex/colourData.csv")
    
    colour_index = feature_names.index('Colour')
    
    gini_results = gini_index_per_feature(data, colour_index)
    
    print(f"\nGini Index for each subclass of 'Colour':")
    for colour, gini in gini_results.items():
        print(f"Colour '{colour}': Gini Index = {gini:.3f}")
