import json

# Read the JSON file
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Replace null values with placeholder strings
for contact in data['contacts']:
    if contact['number'] is None:
        contact['number'] = 'null'
    if contact['company'] is None:
        contact['company'] = 'null'
    if contact['position'] is None:
        contact['position'] = 'null'

# Write back to file
with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=2)

print("✅ Replaced all null values with 'N/A'")