import csv
import json

# Function to convert a CSV file to a JSON file
# Takes the file paths as arguments


def make_json(csvFilePath, jsonFilePath):

    # Create a dictionary
    data = []

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8-sig') as csvf:
        csvReader = csv.DictReader(csvf)

        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            # Create key with "Name" to be the primary key
            data.append(rows)

    # Open a json writer and then use json.dumps() to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

# Driver Code


csvFilePath = r'ophthomedsgrid.csv'
jsonFilePath = r'ophthomedsgrid.json'

# Call the make_jsonfunction
make_json(csvFilePath, jsonFilePath)
