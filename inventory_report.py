import argparse
import sys
import requests
from registry_client import RegistryClient

def fetch_all(client, status=None):
    collected, offset, limit = [], 0, 10
    while True:
        page = client.get_services(limit=limit, offset=offset, status=status)
        collected.extend(page["results"])
        offset += limit
        if offset >= page["count"]:
            break
    return collected

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", default=None) # optional filter
    args = parser.parse_args()
    client = RegistryClient()
    print(args.status) # None when unused
    try:
        services = fetch_all(client, status=args.status)
    except requests.exceptions.RequestException as err:
        print(f"Registry is unreachable")
        sys.exit(1)

    header = f"{'ID':<4} | {'NAME':<20} | {'VERSION':<8} | {'STATUS':<11} | {'ENVIRONMENT':<11}"
    print(header)
    print("-" * len(header))
    if not services:
        print("No services found.")
        return

    for svc in services:
        svc_id = str(svc.get("id", ""))
        name = str(svc.get("name", ""))
        version = str(svc.get("version", ""))
        status = str(svc.get("status", ""))
        env = str(svc.get("environment", ""))
        print(
            f"{svc_id:<4} | {name:<20} | {version:<8} | {status:<11} | {env:<11}")

if __name__ == "__main__":
    main()