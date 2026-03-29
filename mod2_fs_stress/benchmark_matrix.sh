#!/bin/bash

# Shufflecake FS Stress Tester (Module 2)
# Usage: ./benchmark_matrix.sh /mnt/shufflecake_hidden ext4_results.json

TARGET_DIR=$1
OUTPUT_FILE=$2

if [ -z "$TARGET_DIR" ] || [ -z "$OUTPUT_FILE" ]; then
    echo "[!] Usage: $0 <target_mount_point> <output_json_file>"
    echo "    Example: $0 /mnt/sflc_hidden ext4_baseline.json"
    exit 1
fi

if ! command -v fio &> /dev/null; then
    echo "[!] Error: 'fio' is not installed. Please install it (e.g sudo apt install fio)."
    exit 1
fi

echo "[*] Initializing Shufflecake FS Stress Test on: $TARGET_DIR"
echo "[*] Output will be saved to: $OUTPUT_FILE"

# The test matrix: 
# 1. Random Write (High fragmentation stress)
# 2. Sequential Write (Baseline throughput)
# We use 4KB block sizes to match Shufflecake's internal architecture.

fio --name=sflc_random_write \
    --directory="$TARGET_DIR" \
    --ioengine=libaio \
    --rw=randwrite \
    --bs=4k \
    --size=1G \
    --numjobs=4 \
    --iodepth=32 \
    --group_reporting \
    --name=sflc_seq_write \
    --rw=write \
    --bs=1M \
    --size=1G \
    --numjobs=1 \
    --iodepth=16 \
    --output-format=json > "$OUTPUT_FILE"

echo "[*] Benchmark complete. Raw data saved."
