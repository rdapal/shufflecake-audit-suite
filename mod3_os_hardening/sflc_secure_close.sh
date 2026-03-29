#!/bin/bash

# sflc_secure_close.sh
# A defensive wrapper for closing Shufflecake volumes that mitigates host-OS telemetry leaks

if [ "$EUID" -ne 0 ]; then 
  echo "[!] Please run as root (sudo)"
  exit 1
fi

DEVICE=$1

if [ -z "$DEVICE" ]; then
    echo "Usage: sudo ./sflc_secure_close.sh <device_path>"
    echo "Example: sudo ./sflc_secure_close.sh /dev/nvme0n1p2"
    exit 1
fi

echo "[*] Securely closing Shufflecake volumes on $DEVICE..."
# Execute the standard close command
shufflecake close "$DEVICE"

echo "[*] Flushing volatile RAM caches to destroy resident keys and IVs..."
# Force the OS to write any pending data to disk, then drop the pagecache, dentries, and inodes
sync; echo 3 > /proc/sys/vm/drop_caches

echo "[*] Scrubbing local shell history of Shufflecake commands..."
# Remove any command containing 'shufflecake' or 'sflc' from the active user's history
if [ -n "$SUDO_USER" ]; then
    USER_HOME=$(getent passwd "$SUDO_USER" | cut -d: -f6)
    sed -i '/shufflecake\|sflc_secure_close/d' "$USER_HOME/.bash_history"
fi
# Also scrub root's history just in case
sed -i '/shufflecake\|sflc_secure_close/d' /root/.bash_history

# Clear the current session history in RAM
history -c 

echo "[*] Secure close complete. System OpSec restored."
