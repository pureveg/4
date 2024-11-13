def read_csv_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip().split(',') for line in file.readlines()]

def parse_csv(data):
    header = data[0]
    parsed_data = []
    
    for row in data[1:]:
        parsed_row = {header[i]: int(row[i]) for i in range(1, len(header))}
        parsed_row["region"] = row[0]
        parsed_row["total"] = sum(map(int, row[1:]))
        
        parsed_data.append(parsed_row)
    
    return header, parsed_data

def calculate_weights(header, data):
    item_totals = {label: sum(row[label] for row in data) for label in header[1:]}

    print(f"{'Item':<10} {'Region':<10} {'T Weight (%)':<15} {'D Weight (%)':<15} {'Total':<10}")
    print("=" * 65)

    for label in header[1:]:
        for row in data:
            t_weight = (row[label] / row['total'] * 100) if row['total'] else 0
            d_weight = (row[label] / item_totals[label] * 100) if item_totals[label] else 0
            print(f"{label:<10} {row['region']:<10} {t_weight:<15.2f} {d_weight:<15.2f} {row[label]:<10}")
        print()

def main():
    file_path = '5_twt_dwt/Twt_Dwt_IP.csv'
    csv_data = read_csv_file(file_path)
    header, parsed_data = parse_csv(csv_data)
    calculate_weights(header, parsed_data)

main()
