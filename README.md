# pod-catalog
Developed for SkyPilot integration, this repo attempts to convert RunPod cloud offerings into a traditional cloud catalog style.

## Catalog Format

Taken from the v5 SkyPilot format, the catalog is a CSV file with the following columns:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `InstanceType` | string | The type of instance. |
| `vCPUs` | float | The number of virtual CPUs. |
| `MemoryGiB` | float | The amount of memory in GB. |
| `AcceleratorName` | string | The name of accelerators (GPU/TPU). |
| `AcceleratorCount` | float | The number of accelerators (GPU/TPU). |
| `GPUInfo` | string | The human readable information of the GPU (not used in code). |
| `Region` | string | The region of the resource. |
| `AvailabilityZone` | string | The availability zone of the resource (can be empty if not supported in the cloud). |
| `Price` | float | The price of the resource. |
| `SpotPrice` | float | The spot price of the resource. |


## Naming Conventions

**InstanceType** | #x_gpuType

- #x: The number of GPUs
- gpuType: The type of GPU (e.g. v100, p100, k80, etc.)

**vCPUs** | #.0

- #: The number of vCPUs (RunPod does not allow specification of vCPUs but has a minium of 4 per GPU)

**MemoryGiB** | #.0

- #: The amount of memory in GB (RunPod does not allow specification of memory but requires memory to at least match the GPU memory)

**AcceleratorName** | gpuType

GPU types include the following:

- A100
- H100_SXM5
- H100_PCIe
- L40
- RTX_A6000
- RTX_4090
- RTX_3090
- RTX_A4000
- RTX_6000


Removed:

 {
    "location": "US",
    "gpuTypeId": "Tesla V100-SXM2-16GB",
    "gpuTotal": 8
  },
    {
    "location": "RO",
    "gpuTypeId": "Quadro RTX 6000",
    "gpuTotal": 8
  },
