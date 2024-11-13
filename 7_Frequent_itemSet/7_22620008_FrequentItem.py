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

def generate_candidates(prev_frequent_itemsets, k):
    candidates = set()
    prev_frequent_itemsets = list(prev_frequent_itemsets)
    for i in range(len(prev_frequent_itemsets)):
        for j in range(i + 1, len(prev_frequent_itemsets)):
            union_set = prev_frequent_itemsets[i] | prev_frequent_itemsets[j]
            if len(union_set) == k:
                candidates.add(frozenset(union_set))
    return candidates

def calculate_support(transactions, candidates, minsup, total_transactions):
    itemset_support = {}
    for transaction in transactions:
        for candidate in candidates:
            if candidate <= transaction:
                itemset_support[candidate] = itemset_support.get(candidate, 0) + 1
    return {itemset: support / total_transactions for itemset, support in itemset_support.items() if support / total_transactions >= minsup}

def apriori(transactions, minsup):
    total_transactions = len(transactions)
    candidates = [frozenset([item]) for item in set(item for transaction in transactions for item in transaction)]
    freq_itemset, support_data = [], {}

    while candidates:
        frequent_itemsets = calculate_support(transactions, candidates, minsup, total_transactions)
        if not frequent_itemsets:
            break
        freq_itemset.append(frequent_itemsets)
        support_data.update(frequent_itemsets)
        candidates = generate_candidates(frequent_itemsets.keys(), len(list(frequent_itemsets.keys())[0]) + 1)

    return freq_itemset, support_data

def generate_association_rules(freq_itemset, support_data, min_conf):
    rules = []
    for k_itemsets in freq_itemset[1:]:
        for itemset in k_itemsets:
            for antecedent in map(frozenset, [set(itemset) - {i} for i in itemset]):
                consequent = itemset - antecedent
                if consequent:
                    confidence = support_data[itemset] / support_data[antecedent]
                    if confidence >= min_conf:
                        rules.append((antecedent, consequent, confidence))
    return rules

def write_results(filename, freq_itemset, rules):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Frequent Itemsets and Support'])
        for k, k_itemsets in enumerate(freq_itemset, start=1):
            writer.writerow([f"k={k}"])
            for itemset, support in k_itemsets.items():
                writer.writerow([', '.join(itemset), round(support * 100, 2)])

        writer.writerow([])
        writer.writerow(['Association Rules and Confidence'])
        for antecedent, consequent, confidence in rules:
            writer.writerow([', '.join(antecedent), ', '.join(consequent), round(confidence * 100, 2)])

ip = '7_Frequent_itemSet/FrequentItemSet_InputCSV.csv'
op_combined = '7_Frequent_itemSet/FrequentItemSet_and_AssociationRules_OutputCSV.csv'
minsup = float(int(input("Enter the minimum support: "))/100)
min_conf = float(int(input("Enter the minimum confidence: "))/100)

transactions = load_data(ip)
freq_itemset, support_data = apriori(transactions, minsup)
rules = generate_association_rules(freq_itemset, support_data, min_conf)
write_results(op_combined, freq_itemset, rules)
