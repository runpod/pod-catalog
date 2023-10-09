"""Create a catalog for SkyPilot

get_gpu() returns a dictionary with the following keys:
- id: The GPU ID
- displayName: The GPU name
- memoryInGb: The GPU memory in GB
"""

import csv
import json
import runpod

from accelerator_naming import NAME_MAP

REGION_LIST = [
    "US", "NO", "CA", "SE", "IS", "FR", "RO", "CZ", "HR", "NL", "BG"
]

# Obtain the list of GPUs
gpus = runpod.get_gpus()


data = []
for gpu in gpus:
    print(gpu)

    for region in REGION_LIST:
        data.append({
            'gpuTypeId': gpu['id'],
            'location': region
        })


# exit(0)

# gpu = runpod.get_gpu("V100-SXM2-16GB")
# print(gpu)

# with open('resource_location/output_file.json', 'r') as file:
#     data = json.load(file)

csv_data = []
for item in data:
    print(item)
    for size in [1, 2, 4, 8]:
        gpu = runpod.get_gpu(item['gpuTypeId'], size)
        base_entry = {
            'InstanceType': "",
            'vCPUs': float(size * 4),
            'MemoryGiB': float(size * gpu['memoryInGb']),
            'AcceleratorName': NAME_MAP[item['gpuTypeId']],
            'AcceleratorCount': float(size),
            'GpuInfo': gpu['displayName'].replace(" ", "_"),
            'Region': item['location'],
            'Price': 0.0,
            'SpotPrice': 0.0
        }

        if gpu['communityCloud'] and gpu['communityPrice'] and gpu['communitySpotPrice']:
            pass
            # community_entry = base_entry.copy()
            # community_entry['InstanceType'] = f"{size}x_{NAME_MAP[item['gpuTypeId']]}_COMMUNITY"
            # community_entry['Price'] = gpu['communityPrice'] * size
            # community_entry['SpotPrice'] = gpu['communitySpotPrice'] * size
            # csv_data.append(community_entry)

        print(f"Secure: {gpu['secureCloud']}, {gpu['securePrice']}, {gpu['secureSpotPrice']}")

        if gpu['secureCloud'] and gpu['securePrice']:
            secure_entry = base_entry.copy()
            secure_entry['InstanceType'] = f"{size}x_{NAME_MAP[item['gpuTypeId']]}_SECURE"
            secure_entry['Price'] = gpu['securePrice'] * size

            spot_price = gpu['secureSpotPrice'] * size if gpu['secureSpotPrice'] else None
            secure_entry['SpotPrice'] = spot_price

            csv_data.append(secure_entry)


# Create a CSV file
with open('vms.csv', 'w', encoding="UTF-8") as file:
    writer = csv.DictWriter(file, fieldnames=csv_data[0].keys())
    writer.writeheader()
    writer.writerows(csv_data)
