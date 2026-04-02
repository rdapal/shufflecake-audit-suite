import json
import random

print("[*] Generating artificial test data based on expected ShuffleCake cryptographic and I/O behavior...")

# ---------------------------------------------------------
# 1. Mock Entropy Data (For Module 1)
# ---------------------------------------------------------
entropy_data = {}

# Simulate a 2MB file written continuously (512 blocks of 4KB) starting at block index 5000
for i in range(5000, 5512):
    entropy_data[str(i)] = {
        "offset_hex": hex(i * 4096),
        "entropy": round(random.uniform(7.990, 7.999), 4) # AES-CTR encrypted data
    }

# Simulate scattered filesystem journal updates (ext4 metadata)
for i in [10, 11, 15, 1024, 2048]:
    entropy_data[str(i)] = {
        "offset_hex": hex(i * 4096),
        "entropy": round(random.uniform(7.950, 7.990), 4)
    }

with open("synthetic_data/entropy_report.json", "w") as f:
    json.dump(entropy_data, f, indent=4)
print("[+] Created mock 'entropy_report.json'")

# ---------------------------------------------------------
# 2. Mock FIO Benchmark Data (Module 2)
# ---------------------------------------------------------
# fio outputs bandwidth in KB/s.
fio_data = {
    "jobs": [
        {
            "jobname": "sflc_random_write",
            "write": {"bw": 35420} # ~34.5 MB/s
        },
        {
            "jobname": "sflc_seq_write",
            "write": {"bw": 248500} # ~242.6 MB/s
        }
    ]
}

with open("synthetic_data/ext4_results.json", "w") as f:
    json.dump(fio_data, f, indent=4)
print("[+] Created mock 'ext4_results.json'")

print("[*] Ready to test visualize_blocks.py and parse_fio.py!")
