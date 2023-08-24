import json

# Load the JSON data from the file
with open('runpod-gpu-locations.json', 'r') as file:
    data = json.load(file)

# Remove the "count" and "numGpus" keys from each object
new_data = []
for item in data:
    if item['gpuTotal'] < 8:
        continue
    item.pop('count', None)
    item.pop('numGpus', None)

    # Add the modified object to the new list
    new_data.append(item)


# Write the modified JSON data to a new file
with open('output_file.json', 'w') as file:
    json.dump(new_data, file, indent=2)

print("Processed JSON has been saved to output_file.json.")
