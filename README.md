# Shufflecake Defensive Auditing & Hardening Suite

## Project Overview
This repository contains a comprehensive systems and security analysis of the plausible deniability tool **Shufflecake**, as presented in the paper *"Shufflecake: Plausible Deniability for Multiple Hidden Filesystems on Linux"*. 

While Shufflecake successfully achieves single-snapshot security operating at the block layer, plausible deniability does not exist in a vacuum. A secure cryptographic boundary can be compromised by the operational reality of the host environment. This project transitions from cryptographic theory to operational defense, building an auditing suite to test Shufflecake's vulnerabilities and prototyping potential systems-level mitigations to harden the tool.

## Module Architecture

### 1. Multi-Snapshot Entropy Defense (Block attack vector)
Shufflecake does not natively protect against multi-snapshot adversaries because it does not re-randomize actually-free space. We built a forensic tool to mathematically quantify the exact vulnerability window by tracking Shannon entropy degradation across disk images, to visualize how critical the lack of multi-snapshot protection is for plausible deniability.

### 2. File System Configuration Defense (Structural attack vector)
Shufflecake allocates space in slices, which introduces the risk of internal fragmentation. We automate `fio` benchmarking matrices across different filesystems to determine the optimal defensive configuration that minimizes structural metadata leakage through slice allocation patterns.

### 3. Host-OS Hardening Defense (System OpSec)
The host operating system can leak the presence of hidden data when a volume is unlocked. This module provides an automated auditing and mitigation script designed to securely scrub volatile memory, `/var/log`, and swap space immediately upon volume closure. We examine how much leakage we can find and potentially propose patches to harden ShuffleCake's OpSec.
