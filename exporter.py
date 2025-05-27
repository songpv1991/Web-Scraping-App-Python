import csv

def export_to_csv(data, filename="odds_export.csv"):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Match', 'Outcome', 'Market', 'Old', 'New', '% Drop', 'Time'])
            writer.writerows(data)
        print(f"Data exported to {filename}")
    except Exception as e:
        print("Export failed:", e)