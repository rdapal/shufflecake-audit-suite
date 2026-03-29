#!/bin/bash

# Shufflecake Host-OS Telemetry Harvester
# Run this AFTER using and closing a hidden volume to audit potential OpSec leaks

echo "[*] Initializing Host-OS OpSec Audit..."
mkdir -p audit_results

# 1. Check Kernel Logs (dmesg) for device-mapper or loopback creation
echo "[*] Harvesting kernel ring buffer (dmesg)..."
dmesg | grep -i -E "device-mapper|shufflecake|loop|ext4" > audit_results/dmesg_leaks.txt

# 2. Check System Logs for sudo execution and volume mapping
echo "[*] Harvesting /var/log/syslog and auth.log..."
grep -i -E "shufflecake|dm-sflc" /var/log/syslog 2>/dev/null > audit_results/syslog_leaks.txt
grep -i -E "shufflecake|dm-sflc" /var/log/auth.log 2>/dev/null > audit_results/auth_leaks.txt

# 3. Check Bash History
echo "[*] Harvesting local shell history..."
cat ~/.bash_history | grep -i -E "shufflecake|mount|fio" > audit_results/bash_history_leaks.txt

# 4. Check recently used files (GNOME/Desktop environments often cache previews)
echo "[*] Harvesting recently-used metadata..."
cat ~/.local/share/recently-used.xbel 2>/dev/null | grep -i "file://" > audit_results/recent_files_leaks.txt

echo "[*] Audit complete. Review the text files in the 'audit_results' directory."
echo "[!] If these files are not empty, your Plausible Deniability has been potentially compromised by the OS."
