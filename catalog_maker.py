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
        gpu = runpod.get_gpu(item['gpuTypeId'], size)

        new_entry = {}

        new_entry['InstanceType'] = ""
        new_entry['vCPUs'] = float(size * 4)
        new_entry['MemoryGiB'] = float(size * gpu['memoryInGb'])
        new_entry['AcceleratorName'] = NAME_MAP[item['gpuTypeId']]
        new_entry['AcceleratorCount'] = float(size)
        new_entry['Region'] = item['location']

        if gpu['communityCloud'] and gpu['communityPrice'] and gpu['communitySpotPrice']:
            new_entry['InstanceType'] = f"{size}x_{NAME_MAP[item['gpuTypeId']]}_COMMUNITY"
            new_entry['Price'] = gpu['communityPrice']
            new_entry['SpotPrice'] = gpu['communitySpotPrice']
            csv_data.append(new_entry)

        if gpu['secureCloud'] and gpu['securePrice'] and gpu['secureSpotPrice']:
            new_entry['InstanceType'] = f"{size}x_{NAME_MAP[item['gpuTypeId']]}_SECURE"
            new_entry['Price'] = gpu['securePrice']
            new_entry['SpotPrice'] = gpu['secureSpotPrice']
            csv_data.append(new_entry)


# Create a CSV file
with open('vms.csv', 'w', encoding="UTF-8") as file:
    writer = csv.DictWriter(file, fieldnames=csv_data[0].keys())
    writer.writeheader()
    writer.writerows(csv_data)
