import ipaddress
import subprocess
import shutil
import tempfile
import argparse
import os

# Function to get CIDR ranges from file
def get_cidr_ranges(file_path):
    cidr_ranges = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                cidr_input = line.strip()
                if not cidr_input:
                    continue
                try:
                    cidr_ranges.append(ipaddress.IPv4Network(cidr_input, strict=False))
                except ValueError:
                    print(f"Skipping invalid CIDR range: {cidr_input}")
    except FileNotFoundError:
        print(f"[ERROR] CIDR file not found: {file_path}")
        exit(1)
    return cidr_ranges

# Function to get CIDR ranges from manual input
def get_manual_cidr_ranges(manual_ranges):
    cidr_ranges = []
    for cidr_input in manual_ranges:
        try:
            cidr_ranges.append(ipaddress.IPv4Network(cidr_input, strict=False))
        except ValueError:
            print(f"Skipping invalid CIDR range: {cidr_input}")
    return cidr_ranges

# Function to check if an IP is within in-scope CIDR ranges
def check_ip_in_scope(ip, cidr_ranges):
    try:
        ip_obj = ipaddress.IPv4Address(ip)
        return any(ip_obj in cidr for cidr in cidr_ranges)
    except ValueError:
        return False  # Ignore invalid IPs

# Function to resolve subdomains using dnsprobe
def resolve_subdomains(subdomain_file):
    resolved_ips = {}

    if not os.path.exists(subdomain_file):
        print(f"[ERROR] Subdomain file not found: {subdomain_file}")
        exit(1)

    if shutil.which("dnsprobe"):
        try:
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
                with open(subdomain_file, "r") as file:
                    for sub in file:
                        temp_file.write(sub.strip() + "\n")
                temp_file_path = temp_file.name

            result = subprocess.run(["dnsprobe", "-l", temp_file_path], capture_output=True, text=True)

            # Parse dnsprobe output (format: subdomain IP)
            for line in result.stdout.split("\n"):
                parts = line.split()
                if len(parts) == 2:  # Ensure it's a valid "subdomain IP" format
                    subdomain, ip = parts
                    if ip not in resolved_ips:
                        resolved_ips[ip] = []
                    resolved_ips[ip].append(subdomain)

            os.remove(temp_file_path)  # Cleanup temporary file

        except Exception as e:
            print(f"[ERROR] Failed to resolve subdomains: {str(e)}")

    return resolved_ips

# Function to filter in-scope subdomains
def filter_in_scope_subdomains(resolved_ips, cidr_ranges):
    in_scope_subdomains = []
    for ip, subdomains in resolved_ips.items():
        if check_ip_in_scope(ip, cidr_ranges):
            for subdomain in subdomains:
                in_scope_subdomains.append((subdomain, ip))
    return in_scope_subdomains

# Function to save results to a file
def save_results(output_file, in_scope_subdomains):
    try:
        with open(output_file, "w") as file:
            for subdomain, ip in in_scope_subdomains:
                file.write(f"{subdomain}: {ip}\n")
        print(f"[INFO] Results saved to {output_file}")
    except Exception as e:
        print(f"[ERROR] Failed to save results: {e}")

# Argument Parser
parser = argparse.ArgumentParser(
    description="🔍 Filter in-scope subdomains based on CIDR ranges using dnsprobe.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument("-c", "--cidr", help="Path to CIDR file (one CIDR per line).")
parser.add_argument("-m", "--manual", nargs="+", help="Manually enter CIDR ranges (space-separated).")
parser.add_argument("-s", "--subdomains", required=True, help="Path to subdomain list file.")
parser.add_argument("-o", "--output", help="Save results to a specified file.")

args = parser.parse_args()

# Load CIDR ranges from file or manual input
cidr_ranges = []
if args.cidr:
    cidr_ranges.extend(get_cidr_ranges(args.cidr))

if args.manual:
    cidr_ranges.extend(get_manual_cidr_ranges(args.manual))

if not cidr_ranges:
    print("[ERROR] No valid CIDR ranges provided. Use -c or -m.")
    exit(1)

# Resolve subdomains and filter in-scope results
resolved_ips = resolve_subdomains(args.subdomains)
in_scope_subdomains = filter_in_scope_subdomains(resolved_ips, cidr_ranges)

# Always print results to CLI
if in_scope_subdomains:
    print("\n✅ In-scope Subdomains and IPs:")
    for subdomain, ip in in_scope_subdomains:
        print(f"{subdomain}: {ip}")

    # Save results if output option is provided
    if args.output:
        save_results(args.output, in_scope_subdomains)

else:
    print("\n⚠️ No in-scope subdomains found.")

