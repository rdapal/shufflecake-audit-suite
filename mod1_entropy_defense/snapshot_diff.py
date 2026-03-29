import os
import math
import json
import argparse

# Shufflecake explicitly uses 4096-byte blocks to amortize IV overhead
BLOCK_SIZE = 4096 

def calculate_shannon_entropy(data_chunk):
    """Calculates the Shannon entropy of a byte array"""
    if not data_chunk:
        return 0.0
    
    entropy = 0.0
    length = len(data_chunk)
    # Count frequency of each byte (0-255)
    byte_counts = [0] * 256
    for byte in data_chunk:
        byte_counts[byte] += 1
        
    for count in byte_counts:
        if count > 0:
            probability = count / length
            entropy -= probability * math.log2(probability)
            
    return entropy

def diff_snapshots(snap_a_path, snap_b_path):
    """
    Compares two raw disk images block by block
    Returns a dictionary of changed blocks and their new entropy
    """
    changed_blocks = {}
    
    # Ensure both files exist and are the same size
    size_a = os.path.getsize(snap_a_path)
    size_b = os.path.getsize(snap_b_path)
    
    if size_a != size_b:
        print(f"Warning: Snapshots are different sizes! ({size_a} vs {size_b})")
        # For a strict forensic audit, we only compare up to the smaller size
        compare_size = min(size_a, size_b)
    else:
        compare_size = size_a

    total_blocks = compare_size // BLOCK_SIZE

    print(f"[*] Starting block-level diff. Total 4KB blocks to scan: {total_blocks}")

    with open(snap_a_path, 'rb') as fa, open(snap_b_path, 'rb') as fb:
        for block_index in range(total_blocks):
            chunk_a = fa.read(BLOCK_SIZE)
            chunk_b = fb.read(BLOCK_SIZE)

            if chunk_a != chunk_b:
                # Case where plausible deniability is broken
                # We calculate the entropy of the new chunk to confirm it's encrypted data (entropy near 8.0)
                entropy_b = calculate_shannon_entropy(chunk_b)
                
                changed_blocks[block_index] = {
                    "offset_hex": hex(block_index * BLOCK_SIZE),
                    "entropy": round(entropy_b, 4)
                }
                
            # progress indicator
            if block_index % 10000 == 0 and block_index > 0:
                print(f"  ... scanned {block_index}/{total_blocks} blocks")

    return changed_blocks

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shufflecake Multi-Snapshot Entropy Analyzer")
    parser.add_argument("snapshot_a", help="Path to the first (baseline) disk image")
    parser.add_argument("snapshot_b", help="Path to the second (post-write) disk image")
    parser.add_argument("--output", "-o", default="entropy_report.json", help="Output JSON file")
    
    args = parser.parse_args()
    
    print("[*] Initializing Forensic Suite: Module 1...")
    results = diff_snapshots(args.snapshot_a, args.snapshot_b)
    
    print(f"\n[*] Scan Complete. Found {len(results)} changed blocks.")
    
    with open(args.output, 'w') as outfile:
        json.dump(results, outfile, indent=4)
        
    print(f"[*] Results saved to {args.output}. Pass this file to visualize_blocks.py.")
