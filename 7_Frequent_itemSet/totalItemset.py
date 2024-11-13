import csv

def load_data(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = [row for row in reader]
    transactions = [set(row[1:]) - {''} for row in data[1:]]
    return transactions

def generate_itemsets(all_items):
    itemsets = []
    
    def get_combinations(itemset, index):
        if index == len(all_items):
            if itemset:
                itemsets.append(frozenset(itemset))
            return
        get_combinations(itemset + [all_items[index]], index + 1)
        get_combinations(itemset, index + 1)
    
    get_combinations([], 0)
    return itemsets

def count_itemsets(itemsets):
    return len(itemsets)

def write_itemsets_result(filename, itemsets_count, itemsets):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Itemsets', 'Total Itemsets Count'])
        
        for itemset in itemsets:
            writer.writerow([', '.join(itemset),])

ip = '7_Frequent_itemSet/FrequentItemSet_InputCSV.csv'
op_combined = '7_Frequent_itemSet/Itemsets_Count_OutputCSV.csv'

transactions = load_data(ip)

all_items = set(item for transaction in transactions for item in transaction)
itemsets = generate_itemsets(list(all_items))
itemsets_count = count_itemsets(itemsets)

write_itemsets_result(op_combined, itemsets_count, itemsets)

print(f"Total possible itemsets: {itemsets_count}")
