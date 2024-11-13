import csv

def load_data(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = [row for row in reader]
    transactions = [set(row[1:]) - {''} for row in data[1:]]
    return transactions

def calculate_item_frequencies(transactions):
    item_frequency = {}
    for transaction in transactions:
        for item in transaction:
            item_frequency[item] = item_frequency.get(item, 0) + 1
    return item_frequency

def calculate_support(transactions, itemset, total_transactions):
    count = sum(1 for transaction in transactions if itemset <= transaction)
    return count / total_transactions

def calculate_confidence(support_data, antecedent, consequent):
    antecedent_support = support_data.get(antecedent, 0)
    if antecedent_support == 0:
        return 0
    return support_data.get(antecedent | consequent, 0) / antecedent_support

def write_confidence_result(filename, antecedent, consequent, confidence):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Antecedent', 'Consequent', 'Confidence'])
        writer.writerow([', '.join(antecedent), ', '.join(consequent), round(confidence * 100, 2)])

ip = '7_Frequent_itemSet/FrequentItemSet_InputCSV.csv'
op_combined = '7_Frequent_itemSet/AssociationRules_Confidence_OutputCSV.csv'

transactions = load_data(ip)
total_transactions = len(transactions)

antecedent_input = input("Enter the antecedent (comma-separated items): ").split(',')
consequent_input = input("Enter the consequent (comma-separated items): ").split(',')

antecedent = frozenset(antecedent_input)
consequent = frozenset(consequent_input)

item_frequency = calculate_item_frequencies(transactions)

support_data = {}
for item in item_frequency:
    support_data[frozenset([item])] = calculate_support(transactions, frozenset([item]), total_transactions)
support_data[antecedent] = calculate_support(transactions, antecedent, total_transactions)
support_data[antecedent | consequent] = calculate_support(transactions, antecedent | consequent, total_transactions)

confidence = calculate_confidence(support_data, antecedent, consequent)

write_confidence_result(op_combined, antecedent_input, consequent_input, confidence)

print(f"Confidence for rule {', '.join(antecedent_input)} => {', '.join(consequent_input)} is {round(confidence * 100, 2)}%")
