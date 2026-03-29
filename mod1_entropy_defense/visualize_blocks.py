import json
import argparse
import matplotlib.pyplot as plt

def plot_entropy_heatmap(json_path, output_png):
    print(f"[*] Loading entropy data from {json_path}...")
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[!] Error: Could not find {json_path}. Run snapshot_diff.py first.")
        return

    if not data:
        print("[!] No changed blocks found in the JSON to visualize.")
        return

    # Extract data for plotting
    block_indices = [int(k) for k in data.keys()]
    entropies = [v['entropy'] for v in data.values()]

    print(f"[*] Generating visualization for {len(block_indices)} modified blocks...")

    # Set up the plot aesthetics
    plt.figure(figsize=(12, 6))
    
    # Scatter plot with an 'inferno' colormap to highlight high-entropy blocks
    scatter = plt.scatter(block_indices, entropies, c=entropies, cmap='inferno', alpha=0.7, edgecolors='none')
    
    plt.colorbar(scatter, label='Shannon Entropy (Bits/Byte)')
    
    # Draw a threshold line. Encrypted data generally sits above 7.9
    plt.axhline(y=7.9, color='red', linestyle='--', label='Encrypted Data Threshold (~7.9+)')
    
    plt.title('Shufflecake Plausible Deniability Breakage: Multi-Snapshot Block Entropy')
    plt.xlabel('Physical Block Index (4KB granularity)')
    plt.ylabel('Shannon Entropy')
    plt.ylim(0, 8.5)
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)

    # Save the output
    plt.tight_layout()
    plt.savefig(output_png, dpi=300)
    print(f"[*] Visualization saved successfully to {output_png}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize Shufflecake Entropy Leakage")
    parser.add_argument("--input", "-i", default="entropy_report.json", help="Input JSON file")
    # Default output points to the docs folder we created in Commit 1
    parser.add_argument("--output", "-o", default="../docs/entropy_heatmap.png", help="Output PNG image")
    
    args = parser.parse_args()
    plot_entropy_heatmap(args.input, args.output)
