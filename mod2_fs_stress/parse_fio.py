import json
import argparse
import matplotlib.pyplot as plt

def parse_and_plot(json_file, output_png):
    print(f"[*] Parsing fio benchmark data from {json_file}...")
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[!] Error: Could not find {json_file}.")
        return

    jobs = data.get('jobs', [])
    if not jobs:
        print("[!] No job data found in the JSON.")
        return

    job_names = []
    bandwidths_mb = []

    for job in jobs:
        job_names.append(job['jobname'])
        # Extract write bandwidth (fio outputs in KB/s, convert to MB/s)
        bw_kb = job.get('write', {}).get('bw', 0)
        bandwidths_mb.append(bw_kb / 1024)

    print(f"[*] Generating Bandwidth Matrix Plot...")

    # Plotting aesthetics
    plt.figure(figsize=(10, 6))
    bars = plt.bar(job_names, bandwidths_mb, color=['#ff9999', '#66b3ff'])
    
    plt.title('Shufflecake Structural Defense: File System Throughput Bottlenecks')
    plt.ylabel('Write Bandwidth (MB/s)')
    plt.xlabel('Workload Type (4KB Random vs 1MB Sequential)')
    
    # Add data labels on top of the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 2, f'{round(yval, 1)} MB/s', ha='center', va='bottom', fontweight='bold')

    plt.ylim(0, max(bandwidths_mb) * 1.2) # Add some headroom
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(output_png, dpi=300)
    print(f"[*] Benchmark visualization saved to {output_png}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse and plot fio benchmark JSON")
    parser.add_argument("input_json", help="Path to the fio JSON output")
    parser.add_argument("--output", "-o", default="../docs/fs_benchmark.png", help="Output PNG image path")
    
    args = parser.parse_args()
    parse_and_plot(args.input_json, args.output)
