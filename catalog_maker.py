import csv
import json
import runpod

from accelerator_naming import NAME_MAP

runpod.api_key = ""


# Obtain the list of GPUs
# gpus = runpod.get_gpus()

# for gpu in gpus:
#     print(gpu)

# gpu = runpod.get_gpu("V100-SXM2-16GB")
# print(gpu)

with open('resource_location/output_file.json', 'r') as file:
    data = json.load(file)

csv_data = []
for item in data:

    for size in [1, 2, 4, 8]:
        new_entry = {}

        print(f"Processing {item['gpuTypeId']} with {size} GPUs")
        gpu = runpod.get_gpu(item['gpuTypeId'])
        new_entry['InstanceType'] = f"{size}x_{NAME_MAP[item['gpuTypeId']]}"
        new_entry['vCPUs'] = float(size * 4)
        new_entry['MemoryGiB'] = float(size * gpu['memoryInGb'])
        new_entry['AcceleratorName'] = NAME_MAP[item['gpuTypeId']]
        new_entry['AcceleratorCount'] = float(size)
        new_entry['Region'] = item['location']
        new_entry['Price'] = gpu['lowestPrice']['uninterruptablePrice']

        csv_data.append(new_entry)

print(csv_data)

# Create a CSV file
with open('output_file.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=csv_data[0].keys())
    writer.writeheader()
    writer.writerows(csv_data)
